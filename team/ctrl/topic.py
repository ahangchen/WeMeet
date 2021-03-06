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
    return {'id': topic.id, 'title': topic.title, 'content': topic.content,
            'time': '%04d-%02d-%02d-%02d-%02d-%02d' % (
                topic.time.year, topic.time.month, topic.time.day, topic.time.hour, topic.time.minute, topic.time.second
            )
            }


def team_topics(tid):
    topics = Topic.objects.filter(team_id=tid)
    return [
        {
            'topic_id': topic.id,
            'title': topic.title,
            'content': topic.content,
            'time': '%04d-%02d-%02d-%02d-%02d-%02d' % (
                topic.time.year, topic.time.month, topic.time.day, topic.time.hour, topic.time.minute, topic.time.second
            )
        }
        for topic in topics]


def newest():
    topics = Topic.objects.all().order_by('-id')[: 8]
    return [
        {
            'team_logo': topic.team.logo_path,
            'team_name': topic.team.name,
            'team_id': topic.team.id,
            'topic_id': topic.id,
            'topic_title': topic.title,
            'topic_content': topic.content,
            'topic_time': '%04d-%02d-%02d-%02d-%02d-%02d' % (
                topic.time.year, topic.time.month, topic.time.day, topic.time.hour, topic.time.minute, topic.time.second
            )
        }
        for topic in topics
    ]
