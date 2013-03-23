//
//  ESATests.h
//  ESATests
//
//  Created by Billiam on 2013-03-08.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import <SenTestingKit/SenTestingKit.h>
#import <UIKit/UIKit.h>

#import "AppDelegate.h"
#import "ViewController.h"

@interface ESATests : SenTestCase {
    @private
    AppDelegate     *app_delegate;
    ViewController  *view_controller;
    UIView          *view;
    
}

@end
