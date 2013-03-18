//
//  OrgNameEntry.h
//  ESA
//
//  Created by Chris Workman on 2013-03-13.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface OrgNameEntry : NSObject
@property NSString *orgName;
@property NSInteger orgEntityFK;

- (id)initWithEntityFK:(NSInteger)entityFK OrgName:(NSString *)name;

@end
