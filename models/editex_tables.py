from datetime import datetime

""" ACTIVE RECORD """
if not session.pid:
    session.pid = ''
if not session.active_section:
    session.active_sid = ''
    session.active_section = ''

db.define_table('sect',
                Field('sid'),
                Field('title','string'),
                Field('auth_id','integer',default=auth.user_id))

db.define_table('segment',
                Field('section_id',default=session.pid),
                Field('problem',default=session.pnum),
                Field('comp_id'),
                Field('body','text'),
                Field('category','string',default='txt'),
                Field('parent_id',default=session.pid),
                Field('image','upload'),
                Field('status',default='draft'),
                Field('auth_id',default=auth.user_id),
	            Field('time_of',default=datetime.now()),
                Field('has_solution','boolean'),
                Field('request_help','boolean'),
                Field('terminal','boolean'))

""" COMPOUND toi function as linked list for loading """

db.define_table('part',
                Field('problem',default=session.pnum),
                Field('body','text'),
                Field('category','string',default='txt'),
                Field('next_id','reference part',default=None),
                Field('image','upload'),
                Field('parent_id','reference segment',default=session.actseg),
                Field('status',default='draft'))

db.define_table('activity',
                Field('time_of',default=datetime.now()),
                Field('auth_id',default=auth.user_id),
                Field('segment_id',default=session.pid),
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
