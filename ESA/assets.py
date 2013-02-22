# flask_assets help to manage java-script and css files for 
# this flask application. List each category inside each block.

# Bundle functions are disable for compact css and js files. As for 
# this project, its not as important to compact the codes. 

# For Development purpose, compact code would not help for debugging. 

from flask_assets import Bundle


# Add our custom JavaScript files in this bundle below. It will be share to both 
# common_js and qunit_js bundle.
ESA_js = Bundle(
    'jClient/ESA-client.js',

)


# Add unit testing JavaScript files in this bundle below.
unit_test_js = Bundle(
    'unit_test/test_ESA-client.js',

)


# css file for ESA application
common_css = Bundle(
    'bootstrap/css/bootstrap.css',

    # Assets manager output all css files into one css file
    # Bundle(
    #     'css/layout.less',
    #     filters='less'
    # ),
    # filters='cssmin'
    # output='public/css/common.css'

)


# js files for ESA application
common_js = Bundle(
    'jquery/jquery-1.9.1.js',
    'bootstrap/js/bootstrap.js',
    ESA_js,
    # Assets manager output all js file and compress them into one js file
    # Bundle(
    #     'js/main.js',
    #     filters='closure_js'
    # ),
    # output='public/js/common.js'

)


# qunit css bundle for unit testing 
qunit_css = Bundle(
    'qunit/qunit-1.11.0.css',

)


# qunit js bundle for unit testing, including common javascript
qunit_js = Bundle(
    'jquery/jquery-1.9.1.js',
    'bootstrap/js/bootstrap.js',
    'qunit/qunit-1.11.0.js',
    ESA_js,
    unit_test_js,

)
