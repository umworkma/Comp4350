//
//  SignUpViewController.h
//  ESA
//
//  Created by Ryoji Betchaku on 2013-03-16.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "ViewController.h"
#import <RestKit/RestKit.h>
@interface SignUpViewController : ViewController <UITextFieldDelegate>

@property (weak, nonatomic) IBOutlet UITextField *textUsername;
@property (weak, nonatomic) IBOutlet UITextField *textPassword1;
@property (weak, nonatomic) IBOutlet UITextField *textPassword2;

- (IBAction)register:(id)sender;
//@property (copy, nonatomic) NSString *username;
//@property (copy, nonatomic) NSString *password1;
//@property (copy, nonatomic) NSString *password2;


@end
