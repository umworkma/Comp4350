//
//  SignUpViewController.m
//  ESA
//
//  Created by Ryoji Betchaku on 2013-03-23.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "SignUpViewController.h"
#import "Settings.h"
#import "OrgListTableViewViewController.h"


@interface SignUpViewController ()
//- (IBAction)register:(id)sender;
//@property (weak, nonatomic) IBOutlet UITextField *textUsername;
//@property (weak, nonatomic) IBOutlet UITextField *textPassword1;
//@property (weak, nonatomic) IBOutlet UITextField *textPassword2;

@end

@implementation SignUpViewController

@synthesize textUsername;
@synthesize textPassword1;
@synthesize textPassword2;


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
    @try
    {
        // check if user provides all required inputs

        if([textUsername.text length] == 0 || [textPassword1.text length] == 0 || [textPassword2.text length] == 0)
        {
            [self alertStatus: @"Field cannot be empty" : @"Input required"];
        }
        else
        {
            // declare url to connect
            // NSURL *baseURL = [NSURL URLWithString:@"http://ec2-184-73-25-114.compute-1.amazonaws.com"];
            NSURL *baseURL = [NSURL URLWithString:BASE_URL];
            NSURL *url = [NSURL URLWithString:@"/_submit_employee_form" relativeToURL: baseURL];
            
            NSString *user = [textUsername text];
            NSString *pwd = [textPassword1 text];
            
            
            // form an input string including given username and password
            NSString *input = [[NSString alloc] initWithFormat:@"{"
                               @"\"username\":\"%@\",\"password\": \"%@\",\"firstname\": \"%@\",\"lastname\": \"N/A\", \"Entity\":{ \"entity_type\": \"1\", \"addresses\""
                               @":[{\"address1\":\"N/A\", \"address2\":\"N/A\", \"address3\":\"N/A\", \"city\":\"N/A\", \"province\":\"N/A\", \"country\":\"N/A\","
                               @"\"postalcode\":\"N/A\", \"isprimary\":\"True\"}], \"contacts\": [{\"type\": \"1\","
                               @"\"value\":\"N/A\", \"isPrimary\":\"True\"}, {\"type\":\"2\", \"value\": \"N/A\", \"isprimary\":\"False\"}]}}",user,pwd,user];
            
            
            NSData *pData = [input dataUsingEncoding:NSASCIIStringEncoding allowLossyConversion: YES];
            NSString *plength = [NSString stringWithFormat:@"%d", [pData length]];
            
            NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
            [request setURL:url];
            [request setHTTPMethod:@"POST"];
            [request setValue:plength forHTTPHeaderField:@"Content-Length"];
            [request setValue:@"application/json" forHTTPHeaderField:@"Accept"];
            [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
            [request setHTTPBody:pData];
            
            NSError *msg = [[NSError alloc] init];
            NSHTTPURLResponse *response = nil;
            
            NSData *urlData = [NSURLConnection sendSynchronousRequest:request returningResponse:&response error:&msg];
            // check the result from the server
            if([response statusCode] >= 200 && [response statusCode] < 300)
            {
                NSString *responseData = [[NSString alloc] initWithData:urlData encoding:NSUTF8StringEncoding];
                
                SBJsonParser *jsonParser = [SBJsonParser new];
                NSDictionary *jsonData = (NSDictionary *) [jsonParser objectWithString:responseData];
                
                
                NSString *res = (NSString *)[jsonData objectForKey:@"result"];
                
                if([res isEqualToString:@"EmpTrue"])
                {
                    
                    NSString *msg = (NSString *)[[NSString alloc] initWithFormat:@"\nHi %@", user];
                    [self alertStatus:msg :@"Signup Successful"];
                    // go to the org list page 
                    [self.navigationController popToRootViewControllerAnimated:YES];
                    
                }
                else
                {
                    NSString *msg = (NSString *)[jsonData objectForKey:@"msg"];
                    [self alertStatus:msg :@"Signup Failed"];
                }
                
            }
            else
            {
                if(msg) NSLog(@"Error: %@", msg);
                [self alertStatus:@"Connection Failed" :@"Signup Failed"];
                
            }
            
        }
        
    }
    @catch (NSException *e)
    {
        NSLog(@"Exception -> %@", e);
        
    }
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
