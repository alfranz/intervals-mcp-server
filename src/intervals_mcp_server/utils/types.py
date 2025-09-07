from enum import Enum
from typing import Any, Dict, List, Optional, Union
import json

from pydantic import BaseModel, Field, field_validator, model_validator


__all__ = [
    "Option",
    "WorkoutTarget",
    "HrTarget",
    "Intensity",
    "PaceUnits",
    "ValueUnits",
    "Value",
    "Step",
    "SportSettings",
    "WorkoutDoc",
]


class Option(Enum):
    CATEGORY = "category"
    POOL_LENGTH = "pool_length"
    POWER = "power"


class WorkoutTarget(Enum):
    AUTO = "AUTO"
    POWER = "POWER"
    HR = "HR"
    PACE = "PACE"


class HrTarget(Enum):
    LAP = "lap"
    INSTANT = "1s"
    THREE_SECOND = "3s"
    TEN_SECOND = "10s"
    THIRTY_SECOND = "30s"


class Intensity(Enum):
    ACTIVE = "active"
    REST = "rest"
    WARMUP = "warmup"
    COOLDOWN = "cooldown"
    RECOVERY = "recovery"
    INTERVAL = "interval"
    OTHER = "other"


class PaceUnits(Enum):
    SECS_100M = "SECS_100M"
    SECS_100Y = "SECS_100Y"
    MINS_KM = "MINS_KM"
    MINS_MILE = "MINS_MILE"
    SECS_500M = "SECS_500M"


class ValueUnits(Enum):
    PERCENT_MMP = "%mmp"
    PERCENT_HR = "%hr"
    PERCENT_LTHR = "%lthr"
    PERCENT_PACE = "%pace"
    POWER_ZONE = "power_zone"
    HR_ZONE = "hr_zone"
    PACE_ZONE = "pace_zone"
    WATTS = "w"
    PERCENT_FTP = "%ftp"
    CADENCE = "cadence"


class WorkoutType(Enum):
    RIDE = "ride"
    RUN = "run"
    SWIM = "swim"
    ROW = "row"
    WALK = "walk"
    OTHER = "other"


def float_to_str(value: float) -> str:
    """Format the value without decimals if it's a whole number."""
    return str(int(value)) if value.is_integer() else str(value)


class Value(BaseModel):
    """Represents intensity values for a workout step."""
    value: Optional[float] = None
    start: Optional[float] = None
    end: Optional[float] = None
    units: Optional[ValueUnits] = None
    target: Optional[HrTarget] = None
    
    model_config = {
        "use_enum_values": False
    }

    def to_dict(self) -> Dict[str, Any]:
        """Convert Value instance to dictionary for JSON serialization."""
        data: Dict[str, Any] = {}
        if self.value is not None:
            data["value"] = self.value
        if self.start is not None:
            data["start"] = self.start
        if self.end is not None:
            data["end"] = self.end
        if self.units is not None:
            data["units"] = self.units.value if hasattr(self.units, 'value') else str(self.units)
        if self.target is not None:
            data["target"] = self.target.value if hasattr(self.target, 'value') else str(self.target)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Value":
        """Create Value instance from dictionary."""
        kwargs: Dict[str, Any] = {}
        if "value" in data and data["value"] is not None:
            kwargs["value"] = float(data["value"]) if data["value"] != "" else None
        if "start" in data and data["start"] is not None:
            kwargs["start"] = float(data["start"]) if data["start"] != "" else None
        if "end" in data and data["end"] is not None:
            kwargs["end"] = float(data["end"]) if data["end"] != "" else None
        if "units" in data and data["units"] is not None:
            kwargs["units"] = ValueUnits(data["units"]) if isinstance(data["units"], str) else data["units"]
        if "target" in data and data["target"] is not None:
            kwargs["target"] = HrTarget(data["target"]) if isinstance(data["target"], str) else data["target"]
        return cls(**kwargs)
    
    def to_json(self) -> str:
        """Convert Value instance to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "Value":
        """Create Value instance from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def _format_value(self, value: float) -> str:
        if self.units in [
            ValueUnits.PERCENT_HR,
            ValueUnits.PERCENT_MMP,
            ValueUnits.PERCENT_LTHR,
            ValueUnits.PERCENT_PACE,
            ValueUnits.PERCENT_FTP,
        ]:
            return f"{float_to_str(value)}%"
        elif self.units in [
            ValueUnits.POWER_ZONE,
            ValueUnits.HR_ZONE,
            ValueUnits.PACE_ZONE,
        ]:
            return f"Z{float_to_str(value)}"
        elif self.units in [ValueUnits.WATTS]:
            return f"{float_to_str(value)}W"
        elif self.units in [ValueUnits.CADENCE]:
            return f"{float_to_str(value)}rpm"
        return float_to_str(value)

    def _format_units(self) -> str:
        if self.units in [ValueUnits.PERCENT_HR, ValueUnits.HR_ZONE]:
            return "HR"
        elif self.units in [ValueUnits.PERCENT_MMP]:
            return "MMP"
        elif self.units in [ValueUnits.PERCENT_LTHR]:
            return "LTHR"
        elif self.units in [ValueUnits.PERCENT_PACE, ValueUnits.PACE_ZONE]:
            return "Pace"
        elif self.units in [ValueUnits.PERCENT_FTP]:
            return "ftp"
        elif self.units in [ValueUnits.POWER_ZONE]:
            return "W"
        elif self.units in [ValueUnits.CADENCE]:
            return "Cadence"
        return ""

    def __str__(self) -> str:
        val = ""
        if self.start is not None and self.end is not None:
            val += f"{self.start} - {self.end} "
        if self.value is not None:
            val += f"{self._format_value(self.value)} "
        if self.units is not None:
            val += f"{self._format_units()} "
        if self.target is not None:
            val += f"hr={self.target.value} "
        return val.strip()


class Step(BaseModel):
    """Represents a step in a workout."""
    text: Optional[str] = Field(None, description="Text description of the step")
    text_locale: Optional[Dict[str, str]] = Field(None, description="Localized text descriptions")
    duration: Optional[int] = Field(None, description="Duration in seconds")
    distance: Optional[float] = Field(None, description="Distance in meters")
    until_lap_press: Optional[bool] = Field(None, description="Whether step ends when lap button is pressed")
    reps: Optional[int] = Field(None, description="Number of repetitions for nested steps")
    warmup: Optional[bool] = Field(None, description="Whether this is a warmup step")
    cooldown: Optional[bool] = Field(None, description="Whether this is a cooldown step")
    intensity: Optional[Intensity] = Field(None, description="Intensity type")
    steps: Optional[List["Step"]] = Field(None, description="Nested steps for repetition blocks")
    ramp: Optional[bool] = Field(None, description="Whether intensity ramps up/down during the step")
    freeride: Optional[bool] = Field(None, description="Whether this is a freeride section (no ERG control)")
    maxeffort: Optional[bool] = Field(None, description="Whether this is a maximum effort step")
    power: Optional[Value] = Field(None, description="Power target")
    hr: Optional[Value] = Field(None, description="Heart rate target")
    pace: Optional[Value] = Field(None, description="Pace target")
    cadence: Optional[Value] = Field(None, description="Cadence target")
    hidepower: Optional[bool] = Field(None, description="Whether to hide power data")
    # these are filled in with actual watts, bpm etc. when resolve=true parameter is supplied to the endpoint
    _power: Optional[Value] = Field(None, description="Resolved power values")
    _hr: Optional[Value] = Field(None, description="Resolved heart rate values")
    _pace: Optional[Value] = Field(None, description="Resolved pace values")
    _distance: Optional[float] = Field(None, description="Resolved distance value")
    
    model_config = {
        "use_enum_values": False
    }

    def to_dict(self) -> Dict[str, Any]:
        """Convert Step instance to dictionary for JSON serialization."""
        data: Dict[str, Any] = {}
        if self.text is not None:
            data["text"] = self.text
        if self.text_locale is not None:
            data["text_locale"] = self.text_locale
        if self.duration is not None:
            data["duration"] = self.duration
        if self.distance is not None:
            data["distance"] = self.distance
        if self.until_lap_press is not None:
            data["until_lap_press"] = self.until_lap_press
        if self.reps is not None:
            data["reps"] = self.reps
        if self.warmup is not None:
            data["warmup"] = self.warmup
        if self.cooldown is not None:
            data["cooldown"] = self.cooldown
        if self.intensity is not None:
            data["intensity"] = self.intensity.value
        if self.steps is not None:
            data["steps"] = [step.to_dict() for step in self.steps]
        if self.ramp is not None:
            data["ramp"] = self.ramp
        if self.freeride is not None:
            data["freeride"] = self.freeride
        if self.maxeffort is not None:
            data["maxeffort"] = self.maxeffort
        if self.power is not None:
            data["power"] = self.power.to_dict()
        if self.hr is not None:
            data["hr"] = self.hr.to_dict()
        if self.pace is not None:
            data["pace"] = self.pace.to_dict()
        if self.cadence is not None:
            data["cadence"] = self.cadence.to_dict()
        if self.hidepower is not None:
            data["hidepower"] = self.hidepower
        if self._power is not None:
            data["_power"] = self._power.to_dict()
        if self._hr is not None:
            data["_hr"] = self._hr.to_dict()
        if self._pace is not None:
            data["_pace"] = self._pace.to_dict()
        if self._distance is not None:
            data["_distance"] = self._distance
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Step":
        """Create Step instance from dictionary."""
        kwargs: Dict[str, Any] = {}
        if "text" in data:
            kwargs["text"] = data["text"]
        if "text_locale" in data:
            kwargs["text_locale"] = data["text_locale"]
        if "duration" in data:
            kwargs["duration"] = int(data["duration"]) if data["duration"] is not None else None
        if "distance" in data:
            kwargs["distance"] = float(data["distance"]) if data["distance"] is not None else None
        if "until_lap_press" in data:
            kwargs["until_lap_press"] = bool(data["until_lap_press"])
        if "reps" in data:
            kwargs["reps"] = int(data["reps"]) if data["reps"] is not None else None
        if "warmup" in data:
            kwargs["warmup"] = bool(data["warmup"])
        if "cooldown" in data:
            kwargs["cooldown"] = bool(data["cooldown"])
        if "intensity" in data:
            kwargs["intensity"] = Intensity(data["intensity"]) if data["intensity"] is not None else None
        if "steps" in data and data["steps"] is not None:
            kwargs["steps"] = [cls.from_dict(step) for step in data["steps"]]
        if "ramp" in data:
            kwargs["ramp"] = bool(data["ramp"])
        if "freeride" in data:
            kwargs["freeride"] = bool(data["freeride"])
        if "maxeffort" in data:
            kwargs["maxeffort"] = bool(data["maxeffort"])
        if "power" in data and data["power"] is not None:
            kwargs["power"] = Value.from_dict(data["power"])
        if "hr" in data and data["hr"] is not None:
            kwargs["hr"] = Value.from_dict(data["hr"])
        if "pace" in data and data["pace"] is not None:
            kwargs["pace"] = Value.from_dict(data["pace"])
        if "cadence" in data and data["cadence"] is not None:
            kwargs["cadence"] = Value.from_dict(data["cadence"])
        if "hidepower" in data:
            kwargs["hidepower"] = bool(data["hidepower"])
        if "_power" in data and data["_power"] is not None:
            kwargs["_power"] = Value.from_dict(data["_power"])
        if "_hr" in data and data["_hr"] is not None:
            kwargs["_hr"] = Value.from_dict(data["_hr"])
        if "_pace" in data and data["_pace"] is not None:
            kwargs["_pace"] = Value.from_dict(data["_pace"])
        if "_distance" in data:
            kwargs["_distance"] = float(data["_distance"]) if data["_distance"] is not None else None
        return cls(**kwargs)

    def to_json(self) -> str:
        """Convert Step instance to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Step":
        """Create Step instance from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def _format_duration(self) -> str:
        """Format duration into a human-readable string."""
        if self.duration is None:
            return ""
        remaining_duration = self.duration
        val = ""
        if remaining_duration > 3600:
            val += f"{remaining_duration // 3600}h"
            remaining_duration %= 3600
        if remaining_duration > 100 or remaining_duration == 60:
            val += f"{remaining_duration // 60}m"
            remaining_duration %= 60
        if remaining_duration > 0:
            val += f"{remaining_duration}s"
        return val

    def _format_distance(self) -> str:
        """Format distance into a human-readable string."""
        if self.distance is None:
            return ""
        if self.distance < 1000:
            return f"{float_to_str(self.distance)}mtr"
        return f"{float_to_str(self.distance / 1000)}km"

    def __str__(self) -> str:
        return self._str_helper()
        
    def _str_helper(self, nested: bool = False) -> str:
        val = ""
        if self.reps is not None:
            if nested:
                raise ValueError("Nested steps not supported")
            val += f"\n{self.reps}x "
        else:
            if not nested and self.warmup:
                val += "\nWarmup\n"
            if not nested and self.cooldown:
                val += "\nCooldown\n"

            val += ""
            if self.duration is not None:
                val += f"- {self._format_duration()} "
            elif self.distance is not None:
                val += f"- {self._format_distance()} "

            if self.freeride:
                val += "freeride "
            if self.maxeffort:
                val += "maxeffort "
            if self.ramp:
                val += "ramp "
            if self.hidepower:
                val += "hidepower "
            if self.intensity is not None:
                val += f"intensity={self.intensity.value} "

            if self.power is not None:
                val += f"{self.power} "
            if self.hr is not None:
                val += f"{self.hr} "
            if self.pace is not None:
                val += f"{self.pace} "
            if self.cadence is not None:
                val += f"{self.cadence} "
        if self.text is not None:
            val += f"{self.text} "

        if self.reps is not None and self.steps is not None:
            for step in self.steps:
                val += "\n" + step._str_helper(nested=True)
            val += "\n"
        elif not nested and (self.warmup or self.cooldown):
            val += "\n"
        return val


class SportSettings(BaseModel):
    """Sport-specific settings for a workout."""
    # Add fields as needed based on the actual SportSettings class
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert SportSettings instance to dictionary for JSON serialization."""
        return {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SportSettings":
        """Create SportSettings instance from dictionary."""
        return cls()

    def to_json(self) -> str:
        """Convert SportSettings instance to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "SportSettings":
        """Create SportSettings instance from JSON string."""
        return cls.from_dict(json.loads(json_str))


class WorkoutDoc(BaseModel):
    """Document describing a complete workout.
    
    This model represents all aspects of a workout including basic metadata,
    specific workout steps, and event-related information like name and start date.
    """
    # Workout metadata
    name: Optional[str] = Field(None, description="Name of the workout")
    description: Optional[str] = Field(None, description="Workout description")
    description_locale: Optional[Dict[str, str]] = Field(None, description="Localized workout descriptions")
    workout_type: Optional[WorkoutType] = Field(None, description="Type of workout (e.g., Ride, Run, Swim)")
    start_date: Optional[str] = Field(None, description="Start date in YYYY-MM-DD format")
    
    # Workout details
    duration: Optional[int] = Field(None, description="Total duration in seconds")
    distance: Optional[float] = Field(None, description="Total distance in meters")
    moving_time: Optional[int] = Field(None, description="Expected moving time in seconds")
    
    # Athlete-specific parameters
    ftp: Optional[int] = Field(None, description="Functional threshold power in watts")
    lthr: Optional[int] = Field(None, description="Lactate threshold heart rate in bpm")
    threshold_pace: Optional[float] = Field(None, description="Threshold pace in meters/second")
    pace_units: Optional[PaceUnits] = Field(None, description="Units used for pace")
    
    # Configuration
    sportSettings: Optional[SportSettings] = Field(None, description="Sport-specific settings")
    category: Optional[str] = Field("WORKOUT", description="Event category for the API (always 'WORKOUT')")
    target: Optional[WorkoutTarget] = Field(None, description="Primary target type (power, HR, pace)")
    steps: Optional[List[Step]] = Field(None, description="Workout steps")
    zoneTimes: Optional[List[Union[int, Dict[str, Any]]]] = Field(
        None, description="Time spent in each zone (sometimes array of ints, sometimes objects)"
    )
    options: Optional[Dict[str, str]] = Field(None, description="Additional workout options")
    locales: Optional[List[str]] = Field(None, description="Supported locales")
    
    model_config = {
        "use_enum_values": False
    }
    
    @model_validator(mode="after")
    def validate_workout_data(self) -> "WorkoutDoc":
        """Ensure the workout has at least name and workout_type."""
        if self.name is None and self.description is not None:
            # Use description as name if name is not provided
            self.name = self.description.split('\n')[0] if '\n' in self.description else self.description
        
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert WorkoutDoc instance to dictionary for JSON serialization."""
        data: Dict[str, Any] = {}
        if self.name is not None:
            data["name"] = self.name
        if self.description is not None:
            data["description"] = self.description
        if self.description_locale is not None:
            data["description_locale"] = self.description_locale
        if self.workout_type is not None:
            data["workout_type"] = self.workout_type.value if hasattr(self.workout_type, 'value') else str(self.workout_type)
        if self.start_date is not None:
            data["start_date"] = self.start_date
        if self.duration is not None:
            data["duration"] = self.duration
        if self.distance is not None:
            data["distance"] = self.distance
        if self.moving_time is not None:
            data["moving_time"] = self.moving_time
        if self.ftp is not None:
            data["ftp"] = self.ftp
        if self.lthr is not None:
            data["lthr"] = self.lthr
        if self.threshold_pace is not None:
            data["threshold_pace"] = self.threshold_pace
        if self.pace_units is not None:
            data["pace_units"] = self.pace_units.value if hasattr(self.pace_units, 'value') else str(self.pace_units)
        if self.sportSettings is not None:
            data["sportSettings"] = self.sportSettings.to_dict()
        if self.category is not None:
            data["category"] = self.category
        if self.target is not None:
            data["target"] = self.target.value if hasattr(self.target, 'value') else str(self.target)
        if self.steps is not None:
            data["steps"] = [step.to_dict() for step in self.steps]
        if self.zoneTimes is not None:
            data["zoneTimes"] = self.zoneTimes
        if self.options is not None:
            data["options"] = self.options
        if self.locales is not None:
            data["locales"] = self.locales
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkoutDoc":
        """Create WorkoutDoc instance from dictionary."""
        kwargs: Dict[str, Any] = {}
        if "name" in data:
            kwargs["name"] = data["name"]
        if "description" in data:
            kwargs["description"] = data["description"]
        if "description_locale" in data:
            kwargs["description_locale"] = data["description_locale"]
        if "workout_type" in data and data["workout_type"] is not None:
            kwargs["workout_type"] = WorkoutType(data["workout_type"]) if isinstance(data["workout_type"], str) else data["workout_type"]
        if "start_date" in data:
            kwargs["start_date"] = data["start_date"]
        if "duration" in data:
            kwargs["duration"] = int(data["duration"]) if data["duration"] is not None else None
        if "distance" in data:
            kwargs["distance"] = float(data["distance"]) if data["distance"] is not None else None
        if "moving_time" in data:
            kwargs["moving_time"] = int(data["moving_time"]) if data["moving_time"] is not None else None
        if "ftp" in data:
            kwargs["ftp"] = int(data["ftp"]) if data["ftp"] is not None else None
        if "lthr" in data:
            kwargs["lthr"] = int(data["lthr"]) if data["lthr"] is not None else None
        if "threshold_pace" in data:
            kwargs["threshold_pace"] = float(data["threshold_pace"]) if data["threshold_pace"] is not None else None
        if "pace_units" in data and data["pace_units"] is not None:
            kwargs["pace_units"] = PaceUnits(data["pace_units"]) if isinstance(data["pace_units"], str) else data["pace_units"]
        if "sportSettings" in data and data["sportSettings"] is not None:
            kwargs["sportSettings"] = SportSettings.from_dict(data["sportSettings"])
        if "target" in data and data["target"] is not None:
            kwargs["target"] = WorkoutTarget(data["target"]) if isinstance(data["target"], str) else data["target"]
        if "steps" in data and data["steps"] is not None:
            kwargs["steps"] = [Step.from_dict(step) for step in data["steps"]]
        if "zoneTimes" in data:
            kwargs["zoneTimes"] = data["zoneTimes"]
        if "options" in data:
            kwargs["options"] = data["options"]
        if "locales" in data:
            kwargs["locales"] = data["locales"]
        return cls(**kwargs)

    def to_json(self) -> str:
        """Convert WorkoutDoc instance to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "WorkoutDoc":
        """Create WorkoutDoc instance from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def __str__(self) -> str:
        val = ""
        if self.description is not None:
            val += f"{self.description}\n"
        if self.steps is not None:
            for step in self.steps:
                val += step.__str__() + "\n"
        return val
