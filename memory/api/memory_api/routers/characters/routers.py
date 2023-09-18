from fastapi import APIRouter
from .protocol import Character, ChatRequest, ChatMessage
from memory_api.clients.cozo import client


router = APIRouter()


@router.get("/characters/{character_id}")
def get_characters(character_id: str) -> Character:
    query = f"""
    input[character_id] <- [[to_uuid("{character_id}")]]

    ?[
        character_id,
        name,
        about,
        metadata,
        model,
        updated_at,
        created_at,
    ] := input[character_id],
        *characters {{
            character_id,
            name,
            about,
            metadata,
            model,
            updated_at: validity,
            created_at,
            @ "NOW"
        }}, updated_at = to_int(validity)"""

    resp = client.run(query)

    return Character(
        id=resp["character_id"][0],
        name=resp["name"][0],
        about=resp["about"][0],
        metadata=resp["metadata"][0],
        created_at=resp["created_at"][0],
        updated_at=resp["updated_at"][0],
        model=resp["model"][0]
    )


@router.post("/characters/")
def create_character(character: Character) -> Character:
    query = f"""
    {{
        ?[character_id, name, about, metadata, model] <- [
            ["{character.id}", "{character.name}", "{character.about}", {character.metadata}, "{character.model}"]
        ]
        
        :put characters {{
            character_id =>
            name,
            about,
            metadata,
            model,
        }}
    }}

    {{
        ?[
            character_id,
            name,
            about,
            metadata,
            model,
            updated_at,
            created_at,
        ] := *characters {{
            character_id,
            name,
            about,
            metadata,
            model,
            updated_at: validity,
            created_at,
            @ "NOW"
        }}, updated_at = to_int(validity)
    }}"""

    resp = client.run(query)

    return Character(
        id=resp["character_id"][0],
        name=resp["name"][0],
        about=resp["about"][0],
        metadata=resp["metadata"][0],
        created_at=resp["creared_at"][0],
        updated_at=resp["updated_at"][0],
        model=resp["model"][0],
    )


@router.post("/characters/{character_id}/chat")
def character_chat(character_id: str, request: ChatRequest) -> list[ChatMessage]:
    pass
