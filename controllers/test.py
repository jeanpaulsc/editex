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