from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from brobot.services.scenarios import ScenarioService
from brobot.database import get_session

from brobot.dto import ScenarioWithChapterDTO

router = APIRouter()


@router.get("/{scenario_id}", response_model=ScenarioWithChapterDTO)
async def read_scenario(scenario_id: int, session: Session = Depends(get_session)):
    service = ScenarioService(session)
    scenario_db = service.get(scenario_id)
    if not scenario_db:
        raise HTTPException(status_code=404, detail="Unable to find scenario")
    return scenario_db


@router.get("/", response_model=List[ScenarioWithChapterDTO])
async def read_all_scenarios(session: Session = Depends(get_session)):
    """
    Retrieve all scenarios from the database.
    """
    service = ScenarioService(session)
    scenarios = service.get_all()
    return scenarios


@router.delete("/{scenario_id}", status_code=204)
async def delete_scenario_route(
    scenario_id: int, session: Session = Depends(get_session)
):
    """
    Delete a scenario by its ID.
    """
    service = ScenarioService(session)
    success = service.delete(scenario_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Scenario not found")
