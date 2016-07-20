from team.db import team


def info(tid):
    ret = team.info(tid)
    if ret is None:
        return None
    else:
        return {'team': ret}