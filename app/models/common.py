from enum import Enum


class HomeType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    VILLA = "villa"
    STUDIO = "studio"
    TOWNHOUSE = "townhouse"
    SHARED_HOME = "shared_home"
    OFFICE_HOME = "office_home"
    OTHER = "other"


class OwnershipStatus(str, Enum):
    OWNED = "owned"
    RENTED = "rented"
    SHARED = "shared"
    OTHER = "other"


class HomeGoal(str, Enum):
    IMPROVE_ORGANIZATION = "improve_organization"
    USE_SPACE_BETTER = "use_space_better"
    REDUCE_ENERGY_WASTE = "reduce_energy_waste"
    IMPROVE_COMFORT = "improve_comfort"
    PLAN_MAINTENANCE = "plan_maintenance"
    IMPROVE_SECURITY_AWARENESS = "improve_security_awareness"
    PREPARE_FOR_RENOVATION = "prepare_for_renovation"
    MAKE_MORE_ACCESSIBLE = "make_more_accessible"
    CREATE_CALMER_ENVIRONMENT = "create_calmer_environment"
    TRACK_IMPROVEMENTS = "track_improvements"


class RoomType(str, Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    DINING_ROOM = "dining_room"
    HOME_OFFICE = "home_office"
    STUDY = "study"
    BALCONY = "balcony"
    HALLWAY = "hallway"
    STORAGE_ROOM = "storage_room"
    LAUNDRY_ROOM = "laundry_room"
    GUEST_ROOM = "guest_room"
    KIDS_ROOM = "kids_room"
    OUTDOOR_AREA = "outdoor_area"
    OTHER = "other"


class NaturalLightLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT_ATTENTION = "urgent_attention"


class EffortLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FurnitureCategory(str, Enum):
    SOFA = "sofa"
    BED = "bed"
    DESK = "desk"
    CHAIR = "chair"
    DINING_TABLE = "dining_table"
    WARDROBE = "wardrobe"
    CABINET = "cabinet"
    BOOKSHELF = "bookshelf"
    TV_UNIT = "tv_unit"
    COFFEE_TABLE = "coffee_table"
    STORAGE_BOX = "storage_box"
    DRESSER = "dresser"
    KITCHEN_UNIT = "kitchen_unit"
    OTHER = "other"


class ApplianceCategory(str, Enum):
    REFRIGERATOR = "refrigerator"
    AIR_CONDITIONER = "air_conditioner"
    FAN = "fan"
    WASHING_MACHINE = "washing_machine"
    DRYER = "dryer"
    WATER_HEATER = "water_heater"
    OVEN = "oven"
    MICROWAVE = "microwave"
    TELEVISION = "television"
    COMPUTER = "computer"
    LIGHTING = "lighting"
    WATER_PUMP = "water_pump"
    OTHER = "other"


class ConditionLevel(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNKNOWN = "unknown"


class UsageFrequency(str, Enum):
    RARELY = "rarely"
    OCCASIONALLY = "occasionally"
    OFTEN = "often"
    DAILY = "daily"


class HomeStyle(str, Enum):
    MINIMAL = "minimal"
    MODERN = "modern"
    WARM_CONTEMPORARY = "warm_contemporary"
    TRADITIONAL = "traditional"
    JAPANDI = "japandi_inspired"
    INDUSTRIAL = "industrial"
    CLASSIC = "classic"
    ECLECTIC = "eclectic"
    NATURAL = "natural"
    FUNCTIONAL = "functional"
    UNDECIDED = "undecided"


class MaintenanceCategory(str, Enum):
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    HVAC = "hvac"
    ROOF = "roof"
    WALLS_AND_PAINT = "walls_and_paint"
    WINDOWS_AND_DOORS = "windows_and_doors"
    APPLIANCES = "appliances"
    PEST_CONTROL = "pest_control"
    WATER_SYSTEMS = "water_systems"
    SAFETY_EQUIPMENT = "safety_equipment"
    FURNITURE = "furniture"
    OUTDOOR_AREAS = "outdoor_areas"
    OTHER = "other"


class MaintenanceStatus(str, Enum):
    NOT_STARTED = "not_started"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NEEDS_ATTENTION = "needs_attention"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class RecommendationCategory(str, Enum):
    SPACE = "space"
    ORGANIZATION = "organization"
    ENERGY = "energy"
    MAINTENANCE = "maintenance"
    COMFORT = "comfort"
    SAFETY = "safety"
    ACCESSIBILITY = "accessibility"
    IMPROVEMENT = "improvement"


class RecommendationStatus(str, Enum):
    NEW = "new"
    SAVED = "saved"
    COMPLETED = "completed"
    DISMISSED = "dismissed"


class CostType(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
