from datetime import datetime

""" ACTIVE RECORD """
if not session.pid:
    session.pid = ''
if not session.active_section:
    session.active_sid = ''
    session.active_section = ''


db.define_table('sect',
                Field('section_id',default=session.active_sid,requires=IS_NOT_EMPTY),
                Field('title','string'),
                Field('auth_id','integer',default=auth.user_id))

""" COMPOUND to function as linked list for loading """

db.define_table('part',
                Field('problem',default=session.pnum),
                Field('body'), #,requires=IS_NOT_EMPTY),   # should be segment or the word 'image'
                Field('category','string',default='txt'),
                Field('part_id',default=session.part),
                Field('image','upload'),
                Field('parent_num',default=session.pnum),
                Field('parent','reference part',default=None),
                Field('section_id',default=session.section.sid),
                Field('auth_btn',default=None),
                Field('auth_id','integer',default=auth.user_id),
	            Field('time_of',default=datetime.now()))

db.define_table('activity',
                Field('time_of',default=datetime.now()),
                Field('auth_id',default=auth.user_id),
                Field('segment_id',default=session.pid),
                Field('subject','string'))

db.define_table('symchar',
                Field('grp'),
                Field('act','boolean'),
                Field('alt'),
                Field('chr'),
                Field('func'))

db.part.id.readable=db.part.id.writable=False
db.part.category.readable=db.part.category.writable=False
db.part.parent.readable=db.part.parent.writable=False
db.part.auth_id.readable=db.part.auth_id.writable=False
db.part.time_of.readable=db.part.time_of.writable=False
db.activity.time_of.readable=db.activity.time_of.writable=False
db.activity.time_of.readable=db.activity.time_of.writable=False
db.activity.segment_id.readable=db.activity.segment_id.writable=False
db.activity.subject.readable=True
db.activity.subject.writable=False
