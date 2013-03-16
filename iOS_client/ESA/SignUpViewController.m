//
//  SignUpViewController.m
//  ESA
//
//  Created by Ryoji Betchaku on 2013-03-16.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "SignUpViewController.h"

@interface SignUpViewController ()

@property (weak, nonatomic) IBOutlet UITextField *textUsername;
@property (weak, nonatomic) IBOutlet UITextField *textPassword1;
@property (weak, nonatomic) IBOutlet UITextField *textPassword2;

- (IBAction)register:(id)sender;

@end

@implementation SignUpViewController

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

- (IBAction)register:(id)sender {
}

// Method to dismiss the keyboard after users hit return

- (BOOL)textFieldShouldReturn:(UITextField *)textFieldToReturn{
    // check if return is from username field or password field
    if(textFieldToReturn == self.textUsername){
        
        [textFieldToReturn resignFirstResponder];
    }
    else if (textFieldToReturn == self.textPassword1)
    {
        [textFieldToReturn resignFirstResponder];
    }
    else if(textFieldToReturn == self.textPassword2)
    {
        [textFieldToReturn resignFirstResponder];
    }
    return YES;
}



@end
