"""Select dependency-constrained tasks within a resource and deadline budget."""

from graphlib import CycleError, TopologicalSorter
from typing import Annotated, Self

from pydantic import Field, model_validator

from .models import Inputs, Name, Request

PositiveInt = Annotated[int, Field(gt=0, le=10**8)]


class Job(Inputs):
    """An optional job with a duration, one required resource and additive value."""

    duration: PositiveInt
    value: Annotated[int, Field(ge=0, le=10**8)]
    resource: Name
    requires: list[Name] = Field(default_factory=list)


class Schedule(Request):
    """Maximize total job value under unary resource and dependency constraints."""

    deadline: PositiveInt
    reserve: Annotated[int, Field(ge=0)] = 0
    jobs: Annotated[dict[Name, Job], Field(min_length=1)]
    solver_seconds: Annotated[float, Field(gt=0, le=60)] = 2.0

    @model_validator(mode="after")
    def _dependencies(self) -> Self:
        if self.reserve > self.deadline:
            raise ValueError("reserve exceeds deadline")
        if any(not set(j.requires) <= self.jobs.keys() for j in self.jobs.values()):
            raise ValueError("unknown dependency")
        try:
            tuple(
                TopologicalSorter(
                    {n: j.requires for n, j in self.jobs.items()}
                ).static_order()
            )
        except CycleError as error:
            raise ValueError("dependency cycle") from error
        return self

    def calculate(self) -> dict[str, object]:
        """Solve for optional intervals and disclose the optimizer's solution status."""
        from ortools.sat.python import cp_model

        horizon = self.deadline - self.reserve
        model = cp_model.CpModel()
        starts = {n: model.new_int_var(0, horizon, n + "_start") for n in self.jobs}
        chosen = {n: model.new_bool_var(n + "_active") for n in self.jobs}
        resources: dict[str, list[cp_model.IntervalVar]] = {}
        for n, job in self.jobs.items():
            model.add(starts[n] + job.duration * chosen[n] <= horizon)
            interval = model.new_optional_fixed_size_interval_var(
                starts[n], job.duration, chosen[n], n
            )
            resources.setdefault(job.resource, []).append(interval)
            for dep in job.requires:
                model.add(chosen[n] <= chosen[dep])
                order = model.add(starts[n] >= starts[dep] + self.jobs[dep].duration)
                # The native binding has an untyped variadic fallback overload.
                order.only_enforce_if(chosen[n])  # pyright: ignore[reportUnknownMemberType]
        for intervals in resources.values():
            model.add_no_overlap(intervals)
        model.maximize(sum(chosen[n] * j.value for n, j in self.jobs.items()))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.solver_seconds
        solver.parameters.num_search_workers = 1
        status = solver.solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return {"status": solver.status_name(status), "value": None, "jobs": None}
        schedule = {
            n: {
                "start": solver.value(starts[n]),
                "end": solver.value(starts[n]) + j.duration,
                "resource": j.resource,
            }
            for n, j in self.jobs.items()
            if solver.value(chosen[n])
        }
        return {
            "status": solver.status_name(status),
            "value": sum(self.jobs[n].value for n in schedule),
            "jobs": schedule,
            "reserved": self.reserve,
        }
