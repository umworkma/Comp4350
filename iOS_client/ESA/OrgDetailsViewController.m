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
@synthesize text = _text;

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
    // Define the Address mapping from data to an object
    RKObjectMapping *addressMapping = [RKObjectMapping mappingForClass:[Address class]];
    [addressMapping addAttributeMappingsFromDictionary:@{@"addr_entityfk":@"entityFK", @"address1":@"address1", @"address2":@"address2", @"address3":@"address3",
     @"city":@"city", @"province":@"province", @"country":@"country", @"postalcode":@"postalcode", @"isprimary":@"isprimary"}];
    
    // Define the Contact maping from data to an object
    RKObjectMapping *contactMapping = [RKObjectMapping mappingForClass:[Contact class]];
    [contactMapping addAttributeMappingsFromDictionary:@{@"contact_entityfk":@"entityFK", @"type":@"type", @"value":@"value"}];
     
    // Define the Entity mapping from data to an object
    RKObjectMapping *entityMapping = [RKObjectMapping mappingForClass:[Entity class]];
    [entityMapping addAttributeMappingsFromDictionary:@{@"entity_pk":@"pk", @"entity_type":@"type"}];

    // Define the address-entity relationship
    [entityMapping addPropertyMapping:[RKRelationshipMapping relationshipMappingFromKeyPath:@"addresses" toKeyPath:@"addresses" withMapping:addressMapping]];
    
    // Define the contact-entity relationship
     [entityMapping addPropertyMapping:[RKRelationshipMapping relationshipMappingFromKeyPath:@"contacts" toKeyPath:@"contacts" withMapping:contactMapping]];
     
    // Define the Organization mapping from data to an object
    RKObjectMapping *orgMapping = [RKObjectMapping mappingForClass:[Organization class]];
    [orgMapping addAttributeMappingsFromDictionary:@{@"org_entityfk":@"entityFK", @"org_name":@"name", @"org_desc":@"description"}];
    
    // Define the entity-organization relationship
    [orgMapping addPropertyMapping:[RKRelationshipMapping relationshipMappingFromKeyPath:@"Entity" toKeyPath:@"entity" withMapping:entityMapping]];
    
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
    
    // Simplify access to needed data from the organization object retrieved
    NSString *orgName = _org.name;
    NSString *orgDesc = _org.description;
    NSString *addr;
    
    // Get the first address, parse it into accessible string s
    Address *address = [_org.entity.addresses objectAtIndex:0];
    if (address != nil) {
        addr = [[NSString alloc] initWithString:address.address1];
        if (address.address2.length > 0) {
            addr = [NSString stringWithFormat:@"%@<br />%@", addr, address.address2];
        }
        if (address.address3.length > 0) {
            addr = [NSString stringWithFormat:@"%@<br />%@", addr, address.address3];
        }
    addr = [NSString stringWithFormat:@"%@<br />%@, %@, %@<br />%@", addr, address.city, address.province, address.country, address.postalcode];
    }
    else {
        addr = @"No Address on Record";
    }
    
    // Build a string of the available contact methods
    NSString *contacts = [[NSString alloc] init];
    for (Contact *contact in _org.entity.contacts) {
        if (contact != nil) {
            if (contact.type == TYPE_PHONE) {
                contacts = [NSString stringWithFormat:@"%@<strong>Phone:</strong> %@<br />", contacts, contact.value];
            }
            if (contact.type == TYPE_EMAIL) {
                contacts = [NSString stringWithFormat:@"%@<strong>Email:</strong> %@<br />", contacts, contact.value];
            }
        }
    }
     
    NSString *html = [NSString stringWithFormat:@"<p><strong><font size=24>%@</font></strong><br />"
                      @"%@</p>", orgName, orgDesc];
    
    if (addr != nil) {
        html = [NSString stringWithFormat:@"%@<p><strong>Address</strong><br />%@</p>", html, addr];
    }
    
    if (contacts != nil) {
        html = [NSString stringWithFormat:@"%@<p><strong>Contacts</strong><br />%@</p>", html, contacts];
    }
    
    [_text loadHTMLString:html baseURL:nil];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
