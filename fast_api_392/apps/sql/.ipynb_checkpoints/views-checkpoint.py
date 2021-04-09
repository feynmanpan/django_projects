from fastapi.responses import HTMLResponse
#
import apps.sql.config as sqlcfg
####################################################


def dbwtb_isconnected():
    # 確認db連線
    msg = f"dbwtb_isconnected= {sqlcfg.dbwtb.is_connected}"
    return HTMLResponse(msg)
