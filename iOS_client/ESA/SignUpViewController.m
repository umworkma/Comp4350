//
//  SignUpViewController.m
//  ESA
//
//  Created by Ryoji Betchaku on 2013-03-16.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "SignUpViewController.h"

@interface SignUpViewController ()

//@property (weak, nonatomic) IBOutlet UITextField *textUsername;
//@property (weak, nonatomic) IBOutlet UITextField *textPassword1;
//@property (weak, nonatomic) IBOutlet UITextField *textPassword2;

//- (IBAction)register:(id)sender;

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
            NSURL *baseURL = [NSURL URLWithString:@"http://ec2-184-73-25-114.compute-1.amazonaws.com"];
            NSURL *url = [NSURL URLWithString:@"/signup" relativeToURL: baseURL];
           
            NSString *user = [textUsername text];
            NSString *pwd = [textPassword1 text];
            
            
            
            NSString *input = [[NSString alloc] initWithFormat:@"{"
                               @"\"username\":\"%@\",\"password\": \"%@\",\"firstname\": \"a\",\"lastname\": \"a\", \"Entity\":{ \"entity_type\": \"1\", \"addresses\""
                               @":[{\"address1\":\"a\", \"address2\":\"a2\", \"address3\":\"a3\", \"city\":\"city\", \"province\":\"pro\", \"country\":\"c\","
                               @"\"postalcode\":\"a\", \"isprimary\":\"True\"}], \"contacts\": [{\"type\": \"1\","
                               @"\value\":\"1\", \"isPrimary\":\"True\"}, {\"type\":\"2\", \"value\": \"a\", \"isprimary\":\"False\"}]}}", [textUsername text], [textPassword1 text]];
            
            
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
            
            if([response statusCode] >= 200 && [response statusCode] < 300)
            {
                NSString *responseData = [[NSString alloc] initWithData:urlData encoding:NSUTF8StringEncoding];
                
                SBJsonParser *jsonParser = [SBJsonParser new];
                NSDictionary *jsonData = (NSDictionary *) [jsonParser objectWithString:responseData];
                
                NSInteger success = [(NSNumber *) [jsonData objectForKey:@"success"] integerValue];
                if(success == 1)
                {
                    NSString *msg0 = (NSString *)[jsonData objectForKey:@"msg"];
                    NSString *msg1 = (NSString *)[jsonData objectForKey:@"firstname"];
                    NSString *msg2 = (NSString *)[[NSString alloc] initWithFormat:@"%@\nHi %@", msg0, msg1];
                    
                }
                else
                {
                    NSString *msg = (NSString *)[jsonData objectForKey:@"msg"];
                    [self alertStatus:msg :@"Login Failed"];
                }
                
            }
            else
            {
                if(msg) NSLog(@"Error: %@", msg);
                [self alertStatus:@"Connection Failed" :@"Login Failed"];
                
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
