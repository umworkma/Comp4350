//
//  LoginViewController.h
//  ESA
//
//  Created by Billiam on 2013-03-09.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "ViewController.h"
#import <RestKit/RestKit.h>

@interface LoginViewController : ViewController

@property (weak, nonatomic) IBOutlet UITextField *txt_username;
@property (weak, nonatomic) IBOutlet UITextField *txt_password;

-(IBAction)login_btn_touch:(id)sender;

@end
	