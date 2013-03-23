//
//  OrgListTableViewCell.m
//  ESA
//
//  Created by Chris Workman on 2013-03-13.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "OrgListTableViewCell.h"

@implementation OrgListTableViewCell
@synthesize orgName = _orgName;

- (id)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier
{
    self = [super initWithStyle:style reuseIdentifier:reuseIdentifier];
    if (self) {
        // Initialization code
    }
    return self;
}

- (void)setSelected:(BOOL)selected animated:(BOOL)animated
{
    [super setSelected:selected animated:animated];

    // Configure the view for the selected state
}

@end
