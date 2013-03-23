//
//  Address.h
//  ESA
//
//  Created by ShiKage on 2013-03-19.
//  Copyright (c) 2013 SE2. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface Address : NSObject
@property NSInteger pk;
@property NSInteger entityFK;
@property NSString *address1;
@property NSString *address2;
@property NSString *address3;
@property NSString *city;
@property NSString *province;
@property NSString *country;
@property NSString *postalcode;
@property NSInteger isprimary;
@end
