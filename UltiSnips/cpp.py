
import os

# todo make parse object that keeps its data, now it recalculates for each function

# detect e.g. "D:\"
def is_win_drive_letter(string):
    return string[-2:] == ":\\"

def public_api_copyright_notice():
    notice="""
//-------------------------------------------------------------------------
// Name: 
//
//  Copyright 2019 Auro Technologies.  All Rights Reserved.  Auro-3D and 
//  the related symbols are registered trademarks of Auro Technologies. 
//  All materials and technology contained in this work are protected 
//  by copyright law and may not be reproduced, distributed, transmitted, 
//  displayed, published or broadcast, in whole or in part, without the 
//  prior written permission of Auro Technologies NV or in the case of 
//  third party materials, the owner of that content, file and/or method. 
//  You may not alter or remove any trademark, copyright or other notice 
//  from copies of the content, file and/or method.  All other referenced 
//  marks are those of their respective owners.
//  
//  Auro Technologies, phone +32-(0)-14314343, fax +32-(0)-14321224, 
//  www.auro-technologies.com, info@auro-technologies.com.
// 
//-------------------------------------------------------------------------"""
    return notice


# create classname, extension without leading ., and an array of 
# namespaces upto one of the stop_folders
def split_source_fn(path, stop_folders = ['inc', 'src']):
    #folder parts to stop searching for namespaces
    rest_path, fn = os.path.split(path)
    classname, extension = os.path.splitext(fn)
    extension = extension[1:] # remove the leading dot (first char)
    namespaces = []
    # normally we should always encounter a stop_folder,
    # but if we don't, we stop when the path can't be split anymore 
    # TODO:test on posix system, could be it is a single "/"
    while(rest_path and not is_win_drive_letter(rest_path)): 
        rest_path, current = os.path.split(rest_path)
        if(current in stop_folders):
            break
        namespaces.append(current)
    namespaces.reverse()
    return classname, extension, namespaces

import re
def create_include_guard_name(path):
    classname, extension, namespaces = split_source_fn(path)
    include_guard = "HEADER_"
    for ns in namespaces:
        include_guard += ns + "_"
    include_guard += classname + "_" + extension
    include_guard += "_ALREADY_INCLUDED"
    return re.sub(r"[-.]", "_", include_guard)

def create_ns_opening_line(path):
    _, _, namespaces = split_source_fn(path)
    opening_line = ""
    for ns in namespaces:
        opening_line += "namespace " + ns + " { "
    return opening_line.strip()
    
def create_ns_closing_line(path):
    _, _, namespaces = split_source_fn(path)
    closing_line = ""
    for ns in namespaces:
        closing_line += "} "
    return closing_line.strip()

def get_classname(path):
    classname, _, _ = split_source_fn(path)
    return classname

def is_public(path):
    import os
    public_path = os.sep + 'inc' + os.sep
    return public_path in path
