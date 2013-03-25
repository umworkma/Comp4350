//
//  LoginViewController.m
//  ESA
//
//  Created by Billiam on 2013-03-09.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "LoginViewController.h"
#import "Settings.h"

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
    txt_username.delegate = self;
    txt_password.delegate = self;
	// Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


-(IBAction)login_btn_touch:(id)sender {
    @try {
        // check for empty username and password
        if([[txt_username text] isEqualToString:@""] || [[txt_password text] isEqualToString:@""]) {
            [self alertStatus:@"Please enter username and/or password" :@"Input required"];
            
        } else {
            // init url for request
            //NSString *baseURLString = @"http://aws.billiam.ca";
            NSURL *baseURL = [NSURL URLWithString:BASE_URL];
            NSURL *url      = [NSURL URLWithString:@"/login" relativeToURL: baseURL];
            
            // init post request data
            NSString *data          = [[NSString alloc] initWithFormat:@"{\"username\":\"%@\",\"password\":\"%@\"}", [txt_username text], [txt_password text]];
            NSData *postData        = [data dataUsingEncoding:NSASCIIStringEncoding allowLossyConversion:YES];
            NSString *postLength    = [NSString stringWithFormat:@"%d", [postData length]];
            // NSLog(@"PostData: %@", data);

            // init http request object
            NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
            [request setURL: url];
            [request setHTTPMethod:@"POST"];
            [request setValue: postLength forHTTPHeaderField:@"Content-Length"];
            [request setValue:@"application/json" forHTTPHeaderField:@"Accept"];
            [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
            [request setHTTPBody:postData];
            
            // init server return response or error var
            NSError *error = [[NSError alloc] init];
            NSHTTPURLResponse *response = nil;
            
            // send http request and set return var
            NSData *urlData = [NSURLConnection sendSynchronousRequest:request returningResponse:&response error:&error];
            
            if([response statusCode] >= 200 && [response statusCode] < 300) {
                NSString *responseData = [[NSString alloc]initWithData:urlData encoding:NSUTF8StringEncoding];
                //NSLog(@"Server response:\n%@", responseData);
                
                // using SBJson to parse server response
                SBJsonParser *jsonParser = [SBJsonParser new];
                NSDictionary *jsonData = (NSDictionary *) [jsonParser objectWithString:responseData];
                
                // get json success response
                NSInteger success = [(NSNumber *) [jsonData objectForKey:@"success"] integerValue];
                // login successfully 
                if(success == 1) {
                    NSString *msg0 = (NSString *) [jsonData objectForKey:@"msg"];
                    NSString *msg1 = (NSString *) [jsonData objectForKey:@"firstname"];
                    NSString *msg = [[NSString alloc] initWithFormat:@"%@\nHi %@!", msg0, msg1];

                    [self alertStatus:msg :@"Login Success!"];
                    // go to the org list page
                    [self.navigationController popToRootViewControllerAnimated:YES];
                    
                } else {
                    NSString *msg = (NSString *) [jsonData objectForKey:@"msg"];
                    [self alertStatus:msg :@"Login Failed!"];
                    
                }
            } else {
                if (error) NSLog(@"Error: %@", error);
                [self alertStatus:@"Connection Failed" :@"Login Failed!"];
                
            }
        }
    } @catch (NSException * e) {
        NSLog(@"Exception: %@", e);
        [self alertStatus:@"Login Failed." :@"Login Failed!"];
        
    }
    

}

// Method to dismiss the keyboard after users hit return

- (BOOL)textFieldShouldReturn:(UITextField *)textFieldToReturn{
    // check if return is from username field or password field
    if(textFieldToReturn == self.txt_username){
        
        [textFieldToReturn resignFirstResponder];
    }
    else if (textFieldToReturn == self.txt_password)
    {
        [textFieldToReturn resignFirstResponder];
   
    }
    return YES;
}


@end
