import datetime

act_flag = 0

def auth_button():
    return dict()

def index():
    rows = db().select(db.sect.ALL,orderby='section_id')
    print 'leaving index function with ', len(rows)
    return dict(rows=rows)

def view_problems():
    if len(request.args)>0:
        session.active_sid = request.args(0)
        if not session.active_sid:
            redirect('compound','index')
    rows = db(db.part.section_id==session.active_sid).select()
    return dict(rows=rows)

def tex_edit():
    form = SQLFORM.factory()
    return dict()

def append_tex():
    #session.seg_cat = 'tex'
    #if len(request.args)>0:
    parent = request.args(0,cast=int)
    form=SQLFORM(db.part,request.args(0,cast=int))
    form.vars.parent = request.args(0,int)

    if form.process().accepted:
        print "TeX form accepted"
        redirect(URL('compose','view_problems'),client_side=True)
    else:
        print 'error'
        response.flash='failure to insert record'
    return dict(form=form)  #, meta=meta,segs=segs,seg2edit=seg2edit)

@auth.requires_login()
def commit_parts():
    rows = db((db.part.parent==request.args(0))&(db.part.auth_id==auth.user_id)).select()
    rows.update(terminal=True)
    redirect(URL('compose','view_problems', args=form.vars.section_id),client_side=True)

@auth.requires_login()
def append_txt():
    print 'in append_txt'
    if not request.args and not session.pid:
        response.flash='Error: request.args = reference_id omitted'
        redirect('compose','index')
    form = SQLFORM(db.part,formstyle='divs',fields=['body','image','parent'],labels={'body':''})
    if len(request.args)>0:
        form.vars.parent=request.args(0)
    else:
        form.vars.parent=session.pnum
    if form.process().accepted:
        response.flash='record added'
        redirect(URL('compose','view_problems', args=form.vars.section_id),client_side=True)
    return dict(form=form)

@auth.requires_login()
def append_tex():
    print 'in append_tex'
    if not request.args and not session.pnum:
        response.flash='Error: request args omitted'
    form = SQLFORM(db.part,formstyle='divs',labels={'body':""})
    form.vars.id=request.args(0)
    if form.process().accepted:
        response.flash='record added'
    return dict(form=form)

def XXnew_section():
    form=SQLFORM(db.sect)
    if form.process().accepted:
        redirect(URL('compose','section_index',args=form.vars.id))
    return dict(form=form)

def append_problem():
    return "jQuery('#problems').append(%s);" % repr(request.vars.body)

""" WRITE """
@auth.requires_login()
def add_problem():
    print 'entered add_problem'
    body=request.vars.body
    print "body: ",body
    bid = db.segment.insert(body=body)
    print "problem inserted"
    return "jquery('#problems').append(%s);" % body

@auth.requires_login()
def new_problem():
    body=request.vars.body
    form = SQLFORM(db.segment,fields=['body'],formstyle='divs',labels={'body':""})
    if form.process().accepted:
        db(db.segment.id==form.vars.id).update(segnum=form.vars.id)
        response.flash=form.vars.segment_body
    return dict(form=form)

""" READ """
@auth.requires_login()
def show_problem():
    session.cur_owner = ""
    rows = db(db.segment.segnum==request.args(0)).select()
    return dict(rows=rows)

@cache.action()
def download():
    return response.download(request, db)

""" WORKING  """

def form():
    return dict()

def status():
    return dict(request=request, session=session, response=response)

@cache.action(time_expire=5000, cache_model=cache.ram, session=True, vars=False, user_agent=True, public=False)
def textbar():
    rows  = db(db.symchar.act==True).select(orderby='grp')
    d = dict(rows=rows)
    return response.render(d)

def edit_symbols():
    grid = SQLFORM.smartgrid(db.symchar)
    return dict(grid=grid)

def sym_insert():
    sets=dict(greek=['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','ς','τ','υ','φ','χ','ψ','ω'],superscript=['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹','⁺','⁻','⁼','⁽','⁾','ⁿ','ⁱ'],subscript=['₀','₁','₂','₃','₄','₅','₆','₇','₈','₉','₊','₋','₌','₍','₎','ₐ','ₑ','','ᵢ','ⱼ','','ₒ','','ᵣ','ᵤ','ᵥ','ₓ','ₔ'],roots=['√','∛','∜'],numbers=['ℕ','ℤ','ℚ','ℝ','ℂ','∅'],infinity=['∞',' ⧜','⧝','⧞'],multdiv=['×','✕','✖','÷','−','∕','∗','∘','∙','⋅','⋆'],circled=['⊕','⊖','⊗','⊘','⊙','⊚','⊛','⊜','⊝'],squared=['⊞','⊟','⊠','⊡'],elementof=['∈','∋','∉','∌','⋶','⋽','⋲','⋺','⋳','⋻','∊','∍','⋷','⋾','⋴','⋼','⋵','⋸','⋹','⫙','⟒'],binary_rel=['⊂','⊃','⊆','⊇','⊈','⊉','⊊','⊋','⊄','⊅','⫅','⫆','⫋','⫌','⫃','⫄','⫇','⫈','⫉','⫊','⟃','⟄','⫏','⫐','⫑','⫒','⫓','⫔','⫕','⫖','⫗'],setops=['⫘','⋐','⋑','⟈','⟉','∪','⩁','⩂','⩅','⩌','⩏','⩐','∩','⩀','⩃','⩄','⩍','⩎',''],binops=['∖','⩆','⩇','⩈','⩉','⩊','⩋','⪽','⪾','⪿','⫀','⫁','⫂','⋒','⋓'],n_ops=['⋂','⋃','⊌','⊍','⊎','⨃','⨄','⨅','⨆'],joins=['⨝','⟕','⟖','⟗'],pre_succ=['≺','≻','≼','≽','≾','≿','⊀','⊁','⋞','⋟','⋠','⋡','⋨','⋩','⪯','⪰','⪱','⪲','⪳','⪴','⪵','⪶','⪷','⪸','⪹','⪺','⪻','⪼'],lt_gt=['<','>','≮','≯','≤','≥','≰','≱','⪇','⪈','≦','≧','≨','≩'],equal_con=['≝','≞','≟','≠','∹','≎','≏','⪮','≐','≑','≒','≓','≔','≕','≖','≗','≘','≙','≚','≛','≜','⩬','⩭','⩮','⩱','⩲','⩦','⩴','⩵','⩶','⩷','≡','≢','⩧',''],ident_eq=['≍','≭','≣','⩸','≁','≂','≃','≄','⋍','≅','≆','≇','≈','≉','≊','≋','≌','⩯','⩰'],misc_rel=['⊏','⊐','⊑','⊒','⊓','⊔','⋢','⋣','⋤','⋥','⫴','⫵'],logic=['¬','⫬','⫭','⊨','⊭','∀','∁','∃','∄','∴','∵','⊦','⊬','⊧','⊩','⊮','⊫','⊯','⊪','⊰','⊱'],logic_binary=['∧','∨','⊻','⊼','⊽','⋎','⋏','⟑','⟇','⩑','⩒','⩓','⩔','⩕','⩖','⩗','⩘','⩙','⩚','⩛','⩜','⩝','⩞','⩟','⩠','⩢','⩣','⨇','⨈'],logic_nary=['⋀','⋁'],misc_indics=['∎','±','∓','⋮','⋯','⋰','⋱'],ratio=['∝','∶','∷','∺'],angles=['⦜','∟','⊾','⦝','⊿','∠','∡','⦛','⦞','⦟','⦢','⦣','⦤','⦥','⦦','⦧','⦨','⦩','⦪','⦫','⦬','⦭','⦮','⦯','⦓','⦔','⦕','⦖','⟀'],misc_prod=['≀','⨿','⨼','⨽','⧢','⋉','⋊','⋋','⋌'],misc_nary=['∑','⨊','⨁','⨀','⨂','∏','∐','⨉'],single_arrows=['←','→','↑','↓','↔','↕','↖','↗','↘','↙','↚','↛','↮','⟵','⟶','⟷'],double_arrows=['⇐','⇒','⇑','⇓','⇔','⇕','⇖','⇗','⇘','⇙','⇍','⇏','⇎','⟸','⟹','⟺'],misc_arrows=['⇆','⇄','⇅','⇵','⇈','⇊','⇇','⇉'],ascii_brackets=['⟦','⟧','⟨','⟩','⟪','⟫','⟮','⟯','⟬','⟭','⌈','⌉','⌊','⌋','⦇','⦈','⦉','⦊'],full_brackets=['（','）','［','］','｛','｝','｟','｠'],math_brackets=['⟦','⟧','⟨','⟩','⟪','⟫','⟮','⟯','⟬','⟭','⌈','⌉','⌊','⌋','⦇','⦈','⦉','⦊'])
    i = 0
    for key in sets:
        cur_grp = key
        for chr in sets[key]:
            db.symchar.insert(grp=key,chr=chr)
            i = i + 1
    return dict(i=i)