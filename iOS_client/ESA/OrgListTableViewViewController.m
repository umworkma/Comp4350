//
//  OrgListTableViewViewController.m
//  ESA
//
//  Created by Chris Workman on 2013-03-13.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import <RestKit/RestKit.h>

#import "Settings.h"

#import "OrgListTableViewViewController.h"
#import "OrgListTableViewCell.h"
#import "OrgNameEntry.h"

@implementation OrgListTableViewViewController
@synthesize orgNames = _orgNames;

- (id)initWithStyle:(UITableViewStyle)style
{
    self = [super initWithStyle:style];
    if (self) {
        // Custom configuration
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    // Uncomment the following line to preserve selection between presentations.
    // self.clearsSelectionOnViewWillAppear = NO;
 
    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    // self.navigationItem.rightBarButtonItem = self.editButtonItem;
    
    // Configure the datasource
  //  self.orgNames = [[NSMutableArray alloc] init];
  //  [self.orgNames addObject:[[OrgNameEntry alloc] initWithEntityFK:1 OrgName:@"Ai-Kon"]];
  //  [self.orgNames addObject:[[OrgNameEntry alloc] initWithEntityFK:2 OrgName:@"University of Manitoba"]]
    
    // Obtain data from server
    RKObjectMapping *orgnameMapping = [RKObjectMapping mappingForClass:[OrgNameEntry class]];
    [orgnameMapping addAttributeMappingsFromDictionary:@{@"org_name":@"orgName", @"org_entityfk":@"orgEntityFK"}];
    
    RKResponseDescriptor *responseDescriptor = [RKResponseDescriptor responseDescriptorWithMapping:orgnameMapping pathPattern:nil keyPath:@"OrgNames" statusCodes:RKStatusCodeIndexSetForClass(RKStatusCodeClassSuccessful)];
    
    //NSString *baseURLString = @"http://ec2-54-242-137-121.compute-1.amazonaws.com";
    //NSString *baseURLString = @"http://aws.billiam.ca";
    NSURL *baseURL = [NSURL URLWithString:BASE_URL];
    NSURL *url = [NSURL URLWithString:@"/organization" relativeToURL:baseURL];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
//    [request setHTTPMethod:@"GET"];
    [request setValue:@"application/json" forHTTPHeaderField:@"accept"];
//    [request setValue:@"application/json" forHTTPHeaderField:@"content-type"];
//    [request setValue:@"application/json" forHTTPHeaderField:@"accept_mimetypes"];
    
    RKObjectRequestOperation *objectRequestOperation = [[RKObjectRequestOperation alloc] initWithRequest:request responseDescriptors:@[ responseDescriptor ]];
    [objectRequestOperation setCompletionBlockWithSuccess:^(RKObjectRequestOperation *operation, RKMappingResult *mappingResult) {
        RKLogInfo(@"Load collection of organizations: %@", mappingResult.array);
    } failure:^(RKObjectRequestOperation *operation, NSError *error) {
        RKLogInfo(@"Operation failed with error: %@", error);
    }];
    
    [objectRequestOperation start];
    self.orgNames = objectRequestOperation.mappingResult.array;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    // Return the number of sections.
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    // Return the number of rows in the section.
    return [self.orgNames count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"orgTableCell";
    OrgListTableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    
    // Cell configuration
    if (cell == nil) {
        cell = [[OrgListTableViewCell alloc]
                initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier];
    }
    
    OrgNameEntry *org = [self.orgNames objectAtIndex:[indexPath row]];
    NSString *cellValue = org.orgName;
    cell.orgName.text = cellValue;
    
    return cell;
}

/*
// Override to support conditional editing of the table view.
- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the specified item to be editable.
    return YES;
}
*/

/*
// Override to support editing the table view.
- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle forRowAtIndexPath:(NSIndexPath *)indexPath
{
    if (editingStyle == UITableViewCellEditingStyleDelete) {
        // Delete the row from the data source
        [tableView deleteRowsAtIndexPaths:@[indexPath] withRowAnimation:UITableViewRowAnimationFade];
    }   
    else if (editingStyle == UITableViewCellEditingStyleInsert) {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    }   
}
*/

/*
// Override to support rearranging the table view.
- (void)tableView:(UITableView *)tableView moveRowAtIndexPath:(NSIndexPath *)fromIndexPath toIndexPath:(NSIndexPath *)toIndexPath
{
}
*/

/*
// Override to support conditional rearranging of the table view.
- (BOOL)tableView:(UITableView *)tableView canMoveRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the item to be re-orderable.
    return YES;
}
*/

#pragma mark - Table view delegate

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Navigation logic may go here. Create and push another view controller.
    /*
     <#DetailViewController#> *detailViewController = [[<#DetailViewController#> alloc] initWithNibName:@"<#Nib name#>" bundle:nil];
     // ...
     // Pass the selected object to the new view controller.
     [self.navigationController pushViewController:detailViewController animated:YES];
     */
}

@end
