//
//  Contact.h
//  ESA
//
//  Created by ShiKage on 2013-03-19.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface Contact : NSObject
@property NSInteger pk;
@property NSInteger entityFK;
@property NSInteger type;
@property NSString *value;
@property NSInteger isprimary;

#define TYPE_PHONE 1
#define TYPE_EMAIL 2

@end
