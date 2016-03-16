db.define_table('myfile',
        Field('image', 'upload', uploadfield='image_file'),
        Field('image_file', 'blob'))

db.define_table('myform',
               Field('body'),
               Field('image','upload'))