from __future__ import annotations

from dataclasses import dataclass, field
import random

from app.services import menu as menu_service

LOCATIONS = ["Кордон", "Свалка", "Бар"]

RISK_LABELS = {
    1: "низкий",
    2: "средний",
    3: "высокий",
}


@dataclass
class ExploreState:
    current_location: str
    step: int = 0
    fatigue: int = 0
    loot: list[str] = field(default_factory=list)
    last_event: str | None = None


EXPLORE_STATE: dict[int, ExploreState] = {}

EVENT_TEMPLATES: list[dict[str, object]] = [
    {
        "id": "anomaly_glow",
        "title": "Мерцающая аномалия",
        "description": "Впереди видно мерцание воздуха и лежащий на земле болт.",
        "location": "Кордон",
        "risk_level": 2,
        "required_items": [],
        "rewards": ["осколок артефакта"],
        "options": [
            {
                "id": "probe_path",
                "label": "Проверить путь болтом",
                "outcome": "Ты отмечаешь безопасный проход и забираешь осколок.",
                "fatigue_delta": 1,
                "loot_gain": ["осколок артефакта"],
            },
            {
                "id": "detour",
                "label": "Обойти стороной",
                "outcome": "Ты обходишь аномалию, экономя силы.",
                "fatigue_delta": 0,
                "loot_gain": [],
            },
        ],
    },
    {
        "id": "stash_find",
        "title": "Скрытый тайник",
        "description": "В полуразрушенном сарае виден свежий схрон с припасами.",
        "location": "Свалка",
        "risk_level": 1,
        "required_items": [],
        "rewards": ["патроны", "консервы"],
        "options": [
            {
                "id": "take_quick",
                "label": "Быстро забрать",
                "outcome": "Ты хватаешь припасы и уходишь, пока никто не заметил.",
                "fatigue_delta": 1,
                "loot_gain": ["патроны"],
            },
            {
                "id": "inspect_carefully",
                "label": "Осмотреть всё",
                "outcome": "Ты находишь ещё одну банку тушёнки.",
                "fatigue_delta": 2,
                "loot_gain": ["патроны", "консервы"],
            },
        ],
    },
    {
        "id": "bar_mercs",
        "title": "Следы у бара",
        "description": "У входа в Бар видны следы от недавно прошедшего отряда.",
        "location": "Бар",
        "risk_level": 2,
        "required_items": ["патроны"],
        "rewards": ["информация"],
        "options": [
            {
                "id": "follow_tracks",
                "label": "Проследить по следам",
                "outcome": "Ты слышишь переговоры и узнаёшь про свежую точку.",
                "fatigue_delta": 2,
                "loot_gain": ["информация"],
            },
            {
                "id": "wait_inside",
                "label": "Переждать в баре",
                "outcome": "Ты отдыхаешь и собираешь слухи от сталкеров.",
                "fatigue_delta": -1,
                "loot_gain": [],
            },
        ],
    },
]

EVENT_INDEX = {event["id"]: event for event in EVENT_TEMPLATES}


def get_locations() -> list[str]:
    return list(LOCATIONS)


def get_risk_label(level: int) -> str:
    return RISK_LABELS.get(level, "неизвестный")


def _get_state(user_id: int) -> ExploreState:
    if user_id not in EXPLORE_STATE:
        EXPLORE_STATE[user_id] = ExploreState(current_location=LOCATIONS[0])
    return EXPLORE_STATE[user_id]


def _select_event(state: ExploreState) -> dict[str, object]:
    candidates = [
        event
        for event in EVENT_TEMPLATES
        if event["location"] == state.current_location
        and all(item in state.loot for item in event["required_items"])
        and event["id"] != state.last_event
    ]
    if not candidates:
        candidates = [event for event in EVENT_TEMPLATES if event["location"] == state.current_location]
    if not candidates:
        candidates = EVENT_TEMPLATES
    return random.choice(candidates)


def _build_event_options(event: dict[str, object]) -> list[dict[str, str]]:
    options = event.get("options", [])
    return [{"id": option["id"], "label": option["label"]} for option in options]


def start_explore(user_id: int) -> dict[str, object]:
    EXPLORE_STATE[user_id] = ExploreState(current_location=LOCATIONS[0])
    response = next_event(user_id)
    response["message"] = "Ты выходишь в Зону и прислушиваешься к окружающим звукам."
    return response


def next_event(user_id: int) -> dict[str, object]:
    state = _get_state(user_id)
    event = _select_event(state)
    state.step += 1
    state.last_event = event["id"]
    return {
        "event": event,
        "options": _build_event_options(event),
        "message": None,
    }


def resolve_choice(user_id: int, choice_id: str) -> dict[str, object]:
    state = _get_state(user_id)
    event = EVENT_INDEX.get(state.last_event or "")
    if not event:
        return {
            "event": {
                "title": "Вылазка",
                "description": "Ты оглядываешься и ищешь зацепки.",
                "risk_level": 1,
                "rewards": [],
            },
            "message": "Событие потеряно, двигаемся дальше.",
            "options": [{"id": "next", "label": "Продолжить", "callback": "explore_next"}],
        }

    chosen = next(
        (option for option in event.get("options", []) if option["id"] == choice_id),
        None,
    )
    if not chosen:
        return {
            "event": event,
            "message": "Выбор не распознан, попробуй снова.",
            "options": _build_event_options(event),
        }

    fatigue_delta = int(chosen.get("fatigue_delta", 0))
    loot_gain = list(chosen.get("loot_gain", []))
    state.fatigue = max(state.fatigue + fatigue_delta, 0)
    state.loot.extend(loot_gain)
    loot_message = f" Добыча: {', '.join(loot_gain)}." if loot_gain else ""
    message = f"{chosen['outcome']}{loot_message}"
    return {
        "event": event,
        "message": message,
        "options": [
            {"id": "next", "label": "Дальше", "callback": "explore_next"},
            {"id": "exit", "label": "Завершить", "callback": menu_service.BACK_TO_MENU},
        ],
    }


def handle_callback(data: str, user_id: int) -> dict[str, object] | None:
    if data == "explore_start":
        return start_explore(user_id)
    if data == "explore_next":
        return next_event(user_id)
    if data.startswith("explore_choice_"):
        choice_id = data.removeprefix("explore_choice_")
        return resolve_choice(user_id, choice_id)
    return None
