from datetime import datetime

""" ACTIVE RECORD """
if not session.ar:
    session.ar = ''

db.define_table('segment',
                Field('segnum'),
                Field('body','text'),
                Field('category','string',default='txt'),
                Field('parent_id',default=session.ar),
                Field('image','upload'),
                Field('status',default='draft'),
                Field('auth_id',default=auth.user_id),
	            Field('time_of',default=datetime.now()))

db.define_table('activity',
                Field('time_of',default=datetime.now()),
                Field('auth_id',default=auth.user_id),
                Field('segment_id',default=session.ar),
                Field('subject','string'))

db.segment.id.readable=db.segment.id.writable=False
db.segment.category.readable=db.segment.category.writable=False
db.segment.parent_id.readable=db.segment.parent_id.writable=False
db.segment.status.readable=db.segment.status.writable=False
db.segment.auth_id.readable=db.segment.auth_id.writable=False
db.segment.time_of.readable=db.segment.time_of.writable=False
db.activity.time_of.readable=db.activity.time_of.writable=False
db.activity.time_of.readable=db.activity.time_of.writable=False
db.activity.segment_id.readable=db.activity.segment_id.writable=False
db.activity.subject.readable=True
db.activity.subject.writable=False
