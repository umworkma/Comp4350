//
//  OrgDetailsViewController.m
//  ESA
//
//  Created by ShiKage on 2013-03-19.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "OrgDetailsViewController.h"
#import <RestKit/RestKit.h>

#import "Settings.h"

@interface OrgDetailsViewController ()

@end

@implementation OrgDetailsViewController
@synthesize orgName = _orgName;
@synthesize nameLabel;
@synthesize descLabel;

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
    
    // Obtain data from server
    RKObjectMapping *orgMapping = [RKObjectMapping mappingForClass:[Organization class]];
    [orgMapping addAttributeMappingsFromDictionary:@{@"org_entityfk":@"entityFK", @"org_name":@"name", @"org_desc":@"description"}];
    
    RKResponseDescriptor *responseDescriptor = [RKResponseDescriptor responseDescriptorWithMapping:orgMapping pathPattern:@"/organization/:entityFK" keyPath:nil statusCodes:RKStatusCodeIndexSetForClass(RKStatusCodeClassSuccessful)];
    
    NSURL *baseURL = [NSURL URLWithString:BASE_URL];
    NSString *pathString = [NSString stringWithFormat:@"/organization/%d", _orgName.orgEntityFK];
    NSURL *url = [NSURL URLWithString:pathString relativeToURL:baseURL];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    [request setValue:@"application/json" forHTTPHeaderField:@"accept"];
    
    RKObjectRequestOperation *objectRequestOperation = [[RKObjectRequestOperation alloc] initWithRequest:request responseDescriptors:@[ responseDescriptor ]];
    [objectRequestOperation setCompletionBlockWithSuccess:^(RKObjectRequestOperation *operation, RKMappingResult *mappingResult) {
        RKLogInfo(@"Load organization details: %@", mappingResult.firstObject);
    } failure:^(RKObjectRequestOperation *operation, NSError *error) {
        RKLogInfo(@"Operation failed with error: %@", error);
    }];
    
    [objectRequestOperation start];
    _org = objectRequestOperation.mappingResult.firstObject;
    
    // Set view title
    NSString *title = [NSString stringWithFormat:@"About %@", _org.name];
    self.title = title;
    
    // Set name label value
    nameLabel.text = _org.name;
    
    // Set description text
    descLabel.lineBreakMode = NSLineBreakByWordWrapping;
    descLabel.numberOfLines = 0;
    descLabel.text = _org.description;
    
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
