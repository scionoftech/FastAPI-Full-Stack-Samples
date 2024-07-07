from broadcaster import Broadcast
from app.util.deps import get_current_user

broadcaster = None


async def get_broadcaster():
    """

    """
    global broadcaster

    if not broadcaster:
        # https://pypi.org/project.broadcaster
        broadcaster = Broadcast("memory://")

        await broadcaster.connect()

    return broadcaster


