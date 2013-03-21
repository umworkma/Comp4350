//
//  Organization.h
//  ESA
//
//  Created by ShiKage on 2013-03-17.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "Entity.h"

@interface Organization : NSObject
@property NSInteger entityFK;
@property NSString *name;
@property NSString *description;
@property Entity *entity;
@end
