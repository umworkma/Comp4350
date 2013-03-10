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
    @try {
        // check for empty username and password
        if([[txt_username text] isEqualToString:@""] || [[txt_password text] isEqualToString:@""]) {
            [self alertStatus:@"Please enter username and/or password" :@"Input required"];
            
        } else {
            // init url for request
            NSURL *baseURL  = [NSURL URLWithString:@"http://localhost:5000"];
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
                    NSString *msg = (NSString *) [jsonData objectForKey:@"msg"];
                    [self alertStatus:msg :@"Login Success!"];
                    
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



@end
