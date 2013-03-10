//
//  LoginViewController.m
//  ESA
//
//  Created by Billiam on 2013-03-09.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "LoginViewController.h"

@interface LoginViewController ()

@end

@implementation LoginViewController
@synthesize txt_username;
@synthesize txt_password;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


-(IBAction)login_btn_touch:(id)sender {

    // check for empty username and password
    if([[txt_username text] isEqualToString:@""] || [[txt_password text] isEqualToString:@""]) {
        [self alertStatus:@"Please enter username and/or password" :@"Input required"];
        
    } else {
        NSString *msg = [[NSString alloc] initWithFormat:@"Username: %@ \n Passwd: %@", [txt_username text], [txt_password text]];
        [self alertStatus:msg :@"User input"];
        
        
    }
    
}



@end
