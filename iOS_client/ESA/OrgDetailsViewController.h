//
//  OrgDetailsViewController.h
//  ESA
//
//  Created by ShiKage on 2013-03-19.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import <UIKit/UIKit.h>

#import "OrgNameEntry.h"
#import "Organization.h"

@interface OrgDetailsViewController : UIViewController
@property OrgNameEntry *orgName;
@property Organization *org;
@property IBOutlet UILabel *nameLabel;
@property IBOutlet UILabel *descLabel;

@end
