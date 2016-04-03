def index():
    rows = db().select(db.testes.ALL)
    return dict(rows=rows)

def data():
    return dict(form=crud())

def ins():
    rid=db.testes.insert(tsort=1)
    return dict(rid=rid)

def upd():
    rid=db.testes.update(2,sort=3)
    return dict(rid=rid)

def upim():
    stream = open("http://latex.codecogs.com/gif.latex?if%5C%3A%20%5Cexists%20%5C%3A",'rb') #open(filename, 'rb')
    db.myfile.insert(image=stream)
    rows = db(db.images.id>0).select()
    return dict(rows=rows)

def si():
    import urllib
    opener = urllib.FancyURLopener({})
    f = opener.open("http://latex.codecogs.com/gif.latex?if%5C%3A%20%5Cexists%20%5C%3A")
    stream = f.read()
    db.images.insert(image=stream)
    rows = db(db.images.id>0).select()
    return dict(rows=rows)