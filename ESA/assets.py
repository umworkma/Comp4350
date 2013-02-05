from flask_assets import Bundle

common_css = Bundle(
    'bootstrap/css/bootstrap.css',
    # Bundle(
    #     'css/layout.less',
    #     filters='less'
    # ),
    # filters='cssmin'
    # output='public/css/common.css'

)

common_js = Bundle(
    'bootstrap/js/bootstrap.js',
    # Bundle(
    #     'js/main.js',
    #     filters='closure_js'
    # ),
    # output='public/js/common.js'

)
