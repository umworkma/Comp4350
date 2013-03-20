//
//  Entity.h
//  ESA
//
//  Created by ShiKage on 2013-03-19.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Address.h"
#import "Contact.h"

@interface Entity : NSObject
@property NSInteger pk;
@property NSInteger type;
@property NSArray *addresses;
@property NSArray *contacts;
@end
