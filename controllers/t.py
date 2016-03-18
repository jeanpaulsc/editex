def index():
    return dict()

def data():
    print 'data'
    if not session.m:
        session.m = []
    if request.vars.q:
        if len(session.m) == 10:
            del(session.m[0])
        session.m.append(request.vars.q)
    return TABLE(*[TR(v) for v in sorted(session.m)]).xml()

def data2():
    dat = request.args(0)
    print "in /t/data2 with value: ", dat
    if not session.m:
        session.m = []
    if dat:
        if len(session.m) == 10:
            del(session.m[0])
        session.m.append(dat)
    return TABLE(*[TR(v) for v in sorted(session.m)]).xml()

def flash():
    response.flash = 'this text should appear!'
    return dict()


def fade():
    return dict()

def store():
    stream = open(filename, 'rb')
    db.myfile.insert(image=db.myfile.image.store(stream, filename), image_file=stream.read())
    return dict()

def retrieve():
    row = db(db.myfile).select().first()
    (filename, stream) = db.myfile.image.retrieve(row.image)
    import shutil
    shutil.copyfileobj(stream,open(filename,'wb'))
    return dict()

def formlist():     # args:  /section/problem/sub1/sub2
    return dict()

def ajax():
    return dict()

def form1():
    print 'in controller: form2'
    form = SQLFORM(db.myform)
    rows = db(db.myform.id>0).select()
    if form.process().accepted:
        return LOAD('t','form1',ajax=True,ajax_trap=True)
    return dict(form=form,rows=rows)

def form2():
    print 'in controller: form2'
    form = SQLFORM(db.myform)
    rows = db(db.myform.id>0).select()
    if form.process().accepted:
        return LOAD('t','form1',ajax=True,ajax_trap=True)
    return dict(form=form,rows=rows)

def dbmyform():
    form = SQLFORM(db.myform)
    rows = db(db.myform.id>0).select()
    return dict(rows=rows,form=form)

def form5():
    form=SQLFORM(db.myform)
    return dict(form=form)


@cache.action()
def download():
    return response.download(request, db)
