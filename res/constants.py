# directories
LOCAL_DB_DIR = 'res/local_db.db'
UI_FILE_DIR = 'res/ui_main.ui'

# colours
DAY_BAR_ACTIVE = '#72eb3a'
DAY_BAR_INACTIVE = '#353535'

TASK_TEXT_COMPLETED = '#365a08'
TASK_TEXT_INCOMPLETE = 'white'


# sizes
SIDE_MENU_MIN = 50
SIDE_MENU_MAX = 200

# database tables
WEEKDAY_TABLE_NAME = "weekday_tasks"
DATES_TABLE_NAME = "dates_tasks"
CYCLE_TABLE_NAME = "cycle_tasks"

# database table columns
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
WEEKDAY_TABLE_COLUMN_NAMES = ["title", "description", "date_last_done", "mon", "tue", "wed", "thu", "fri", "sat", "sun", "days_rollover"]
WEEKDAY_TABLE_COLUMN_TYPES = ["text", "text", "text", "integer", "integer", "integer", "integer", "integer", "integer", "integer", "integer"]

# notice messages
NOTICE_NONE = ""
NOTICE_WELCOME = "Welcome Back!"

# widget names
WEEKDAY_TITLE_LABELS = ['lbl_monday', 'lbl_tuesday', 'lbl_wednesday', 'lbl_thursday', 'lbl_friday', 'lbl_saturday', 'lbl_sunday']
WEEKDAY_UNDER_FRAMES = ['frm_monday_under', 'frm_tuesday_under', 'frm_wednesday_under', 'frm_thursday_under', 'frm_friday_under', 'frm_saturday_under', 'frm_sunday_under']
WEEKDAY_CHECKBOXES = ['chk_monday_new', 'chk_tuesday_new', 'chk_wednesday_new', 'chk_thursday_new', 'chk_friday_new', 'chk_saturday_new', 'chk_sunday_new']

WEEKDAY_NEW_TASK_TILES = ['frm_monday_new_tile', 'frm_tuesday_new_tile', 'frm_wednesday_new_tile', 'frm_thursday_new_tile', 'frm_friday_new_tile', 'frm_saturday_new_tile', 'frm_sunday_new_tile']
WEEKDAY_NEW_TASK_CHECKBOXES = ['chk_monday_new', 'chk_tuesday_new', 'chk_wednesday_new', 'chk_thursday_new', 'chk_friday_new', 'chk_saturday_new', 'chk_sunday_new']

