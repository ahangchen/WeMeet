from team.models import Topic, Team


def new(tid, title, content):
    team = Team.objects.filter(id=tid).first()
    topic = Topic(team=team, title=title, content=content)
    topic.save()
    return topic.id


def remove(topic_id):
    topic = Topic.objects.filter(id=topic_id)
    topic.delete()
    return 0


def update(topic_id, title, content):
    Topic.objects.filter(id=topic_id).update(title=title, content=content)
    return 0


def get(id):
    topic = Topic.objects.filter(id=id).first()
    return {'id': topic.id, 'title': topic.title, 'content': topic.content}


def list(tid):
    topics = Topic.objects.filter(team_id=tid)
    return [{'topic_id': topic.id, 'title': topic.title, 'content': topic.content} for topic in topics]