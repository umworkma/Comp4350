//
//  OrgNameEntry.m
//  ESA
//
//  Created by Chris Workman on 2013-03-13.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import "OrgNameEntry.h"

@implementation OrgNameEntry
@synthesize orgName = _orgName;
@synthesize orgEntityFK = _orgEntityFK;

- (id)initWithEntityFK:(NSInteger)entityFK OrgName:(NSString *)name
{
    self = [super init];
    self.orgEntityFK = entityFK;
    self.orgName = name;
    
    return self;
}
@end

