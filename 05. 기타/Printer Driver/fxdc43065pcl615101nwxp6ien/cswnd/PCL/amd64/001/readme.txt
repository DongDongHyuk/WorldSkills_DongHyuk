===============================================================================
License Agreement
===============================================================================

1. PROPRIETARY RIGHTS: Title, ownership rights, and intellectual
   property rights in the SOFTWARE shall remain in Fuji Xerox and
   its third party suppliers. You have no rights in the SOFTWARE
   except as expressly granted in accordance with this agreement.

2. LICENSE:  Under this agreement, you are granted a non-exclusive
   license to use the SOFTWARE for the purpose of using with
   compatible Fuji Xerox products in your country. You are not permitted to
   (1) assign, sublicense, sell, rent, lease, convey, or transfer the
   SOFTWARE to any third party by any tangible media such as floppy
   disk, magnetic tape, or CD-ROM, (2) distribute the SOFTWARE on a
   network or by a telephone line available to the public or (3)
   alter, modify, decompile, disassemble, reverse engineer, or create
   derivative works based on the whole or any part of the SOFTWARE.
   If any direction on usage or restriction for the SOFTWARE is
   expressly specified in this web site, you are required to follow
   such direction.

3. TERM: This agreement is effective upon installing the SOFTWARE
   until you terminate the agreement by destroying the SOFTWARE.
   This agreement will also terminate if you fail to abide by any
   terms of this agreement. In case of termination, you must
   promptly destroy the SOFTWARE.

4. LIMITED WARRANTIES: THE SOFTWARE IS SUPPLIED STRICTLY ON AN
   'AS IS' BASIS WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF
   MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, WITH RESPECT
   TO THE SOFTWARE. YOU ARE RESPONSIBLE FOR CHOOSING, MAINTAINING AND
   MATCHING OTHER HARDWARE AND SOFTWARE COMPONENTS IN COMBINATION OF
   THE SOFTWARE. IN NO EVENT, SHALL FUJI XEROX, FUJI XEROX CHANNEL
   PARTNERS, AUTHORIZED DEALERS AND THEIR THIRD PARTY SUPPLIERS BE
   LIABLE FOR ANY LOSS OR DAMAGE INCLUDING INCIDENTAL OR
   CONSEQUENTIAL LOSS OR DAMAGE, ARISING FROM USE OF OR INABILITY TO
   USE SOFTWARE, OR ANY MODIFICATION OF THE SOFTWARE.

5. EXPORT CONTROL: You are not allowed to export the SOFTWARE in part
   or whole, directly or indirectly, in violation of any
   restrictions, laws or regulations imposed by the government of
   your country or any other relevant countries, and are required to obtain
   necessary approval prior to exporting the SOFTWARE.

===============================================================================
PCL 6 Print Driver Ver.6.4.8 Additional Information
===============================================================================

This document provides information about the driver on the
following items:

1. Target Hardware Products
2. Requirements
3. General Comments
4. Limitations
5. Software Update

---------------------------------------------------
1. Target Hardware Products
---------------------------------------------------
FUJI XEROX ApeosPort-IV 3065
           ApeosPort-IV 3060
           ApeosPort-IV 2060
           DocuCentre-IV 3065
           DocuCentre-IV 3060
           DocuCentre-IV 2060

---------------------------------------------------
2. Requirements
---------------------------------------------------
Please note that this print driver operates on a computer running on
the following operating system.

    Microsoft(R) Windows(R) XP Professional x64 Edition
    Microsoft(R) Windows Server(R) 2003 x64 Editions
    Microsoft(R) Windows Vista(R) x64 Editions
    Microsoft(R) Windows Server(R) 2008 x64 Editions
    Microsoft(R) Windows(R) 7 x64 Editions
    Microsoft(R) Windows Server(R) 2008 R2
    Microsoft(R) Windows(R) 8 x64 Editions
    Microsoft(R) Windows Server(R) 2012
    Microsoft(R) Windows(R) 8.1 x64 Editions
    Microsoft(R) Windows Server(R) 2012 R2
    Microsoft(R) Windows(R) 10 x64 Editions

  Please visit our web site to check the latest software and supported
  operating systems.

---------------------------------------------------
3. General Comments
---------------------------------------------------
* Close all the running applications before installing the print driver.

* Always reboot the computer after installing an upgraded version of the print
  driver.

* If you have deleted an older version of the print driver, always reboot the
  computer before installing the new version.

* Some applications provide printing options pertaining to the number of copies
  and collated copies. Always select the printing options in the application
  unless the instructions specify otherwise. Use the print driver dialogs to
  select advanced options such as 2 Sided Print, Sample Set or options that
  are not available in the application.

* Always close the print driver dialogs and/or the application Print dialog box
  before you make any changes to the default settings of the print driver via
  the Control Panel.

* If your Job Offset output does not work well with the collated copies, you
  may try to deselect the "Collate" option in the application and check the
  "Collate" check box in the print driver.

* If a Fax Phonebook is not initialized or created by the current user, he/she
  may not be granted the authority to access it. For such inappropriate access
  by users, the driver will display an error message indicating that the default
  Fax Phonebook cannot be located or the specified Fax Phonebook cannot be
  recognized.
  On the other hand, if a user would like his/her Fax Phonebook to be accessed
  by other users, he/she has to specify the groups and users whose access
  he/she wants to allow, and must grant them at least the 'Change' permission
  to the Fax Phonebook data file.

* A fax job has to be sent separately to each recipient who is specified with 
  the F-code, Password or secure send attributes.
  Otherwise, the printer always disregards the F-code, Password and secure send
  attributes when sending a fax job to multiple recipients. The transmitted job
  is always printed directly at all specified destinations.

* For the installation through the networks on Windows Vista, if you right-click
  on [Printer] folder, go to [Run as administrator] from the menu and select
  [Add printer...], printer icon may not be generated.

* Rename a Printer Icon should comply OS file naming convention. Use Symbols or
  special characters may incur renaming error or unexpected print driver
  behavior.

* Before installing a print driver in the Windows cluster environment, you need
  to install it on each node in the cluster.

---------------------------------------------------
4. Limitations
---------------------------------------------------
* On Microsoft Windows 7 or later versions select a printer from the [Devices
  and Printers] folder. Select Property of the printer and click the [Change
  Sharing Options] button on the [Sharing] tab.
  Then, specify Custom Paper Size.

* Default resolution of this driver is 600dpi. (Denoted by Auto.)
  When outputting through a driver, of which resolution is different from the
  one of this driver, errors such as the followings may be observed depending
  on specifications or limitations of an application.
  - Printed layout of the documents is changed.
  - Printed result of lines or patterns is changed.
  - Unnecessary lines are printed on the output.
  - Necessary lines are not printed on the output.

  In such case, the status may be improved by changing the settings of
  [Resolution] on the [Advanced] tab.

* When the output image of patterns or graphics is different from what you see
  on the screen, the discrepancy may be dissolved by setting the items in the
  [Image Options] tree on the [Advanced] tab as below.
  - Set [High Speed Image Processing] to [Off].
  - Set [Draw the Pattern with the Resolution] to [On].
  - Change [Resolution].
  - Change [Halftone Print].
  Changing the following settings on the [Image Options] tab may also make an
  improvement.
  - Change [Image Quality].
  - Change [Lightness] and [Contrast] in the [Image Settings] dialog box.

* Blank Separators
  If you set [EMF Spooling] to [Enabled] or specify Header, Footer and Watermark,
  and perform [2-Sided Print] with documents of odd number of pages, a blank page
  may be inserted on the last page depending on application or OS.

* The print layout may be changed when you change the [Image Quality] in the
  [Image Options] tab.

* Depending on the application, if the resolution of the driver is high, the
  size of the print data may become huge and printing cannot be done properly.
  When this happens, specify the following settings:
  - Specify the [Resolution] in the [Image Options] group in the [Advanced] tab
    to [300dpi] or [200dpi].

* When printing from the application of QuarkXPress 6.1E, if the [Image Quality]
  setting is [High Resolution] and the resolution of the driver is [1200dpi],
  the document may be printed as blank pages. This issue can be avoided by
  changing the resolution of the driver to [Auto].

* For some applications, if a pasted image is printed at high resolution, the
  print data expands and may result in an extremely slow printing speed.
  The print data size of the output may be improved by changing the following
  settings of [Image Options] group on the [Advanced] tab.
  - Specify the [Image Compression] to [Standard] or [Photo] or [Resolution] to
    [300dpi] or [200dpi].

* When doing a print job by specifying Paper Source as Auto, be sure to set
  Paper Size in the application to the Paper Size that the driver supports to
  enable the automatic paper feed feature.

* When using the Form Overlay feature, use form data of the same Paper Size,
  Resolution, and Image Settings as those of the document you want to print.
  If these settings are different between form data and the page where the form
  data is incorporated, expected print results may not be obtained.

* When using Form Overlay, as some applications paint the background in white
  to print, forms with overlay may be hidden. Such applications include
  Internet Explorer and WordPad.

* With Adobe PageMaker, when this printer is specified for [Compose to printer],
  a layout may change in printing. This issue can be avoided by performing the
  following steps;

  <1> Do not set [Compose to printer].
  <2> Change the [Margins] setting in advance in the printer folder.

* The print result may overlap if Pages Per Sheet (N-Up) and Margins [Standard]
  are selected when printing a document that has exceeded the print area of the
  print driver. When this happens, choose [None] of the [Margins] radio button
  group on the [Image Options] tab.

* When you cancel a fax job in progress from the driver, the application may
  display a warning dialog box. It may indicate a printer error message,
  although there is no error in the printer. In this case, ignore the warning
  message and continue operation.

* To use the [Store in Remote Folder] feature, you must obtain the be
  registered recipient's folder number and passcode in advance.
  Refer to the machine administrator guide on how to create a folder.
* Depending on the application used by the customer, blank pages for page
  adjustment will be inserted automatically according to the conditions like
  the number of copies specified when outputting 2-sided prints.
  In this case, the blank inserts will be included by the application.
  The performance may be improved by changing the setting below.
  - Check [Skip Blank Pages] on [Advanced] tab.

* Even with [Skip Blank Pages] selected, blank pages may still be printed in
  the following situations.
  - The page contains only line feeds.
  - The page contains only spaces.
  - The page contains only line feeds and spaces.
  - A white background drawing instruction is sent from the application.

* With Microsoft Word, even if [Skip Blank Pages] is specified, when a blank
  page is included in documents, it may be output.

* For customers using Microsoft Windows Server 2003 or
  Microsoft Windows Server 2008 Cluster Environment

  <1> To specify custom paper size in a cluster environment, specify a common
      setting for all physical nodes in the cluster environment.

  <2> When [Search Printer] dialog box appears at the press of the [Get
      Information from Printer] button, enter the printer network address.

  <3> Deleting driver in cluster environment
      Microsoft Windows Server 2003 or Microsoft Windows Server 2008
        After the driver on the virtual server is deleted, delete the drivers
        on all standby nodes.
         ** Deleting driver from the standby node
         (1) Change the standby node to active node.
         (2) Install printer on virtual server.
         (3) Delete driver from virtual server.

  <4> Deleting driver
      After the printer icon is deleted, delete the driver from [Server
      Properties]. Then, restart the computer.

* [Cancel] button on [User Details Setup] Dialog
  For some applications, if [Enter User Details] dialog is cancelled when
  printing with the settings of [Prompt User for Entry when Submitting job] on
  [User Details Setup] dialog, a warning dialog may be displayed.
  This warning dialog may indicate a printer error, however, the printer
  actually has no problem.

  In that case, ignore the warning and continue.

* When [EMF Spooling] of [Advanced] tab is set to [Disabled], some documents
  with complex structure may have troubles such as distorted output image and
  failure of the output.

* To change the settings of Custom Paper Size, you need the Administrator
  access rights. On Windows Vista, select printer from the printer folder,
  right-click to go [Run as administrator] and select [Properties].
  After clicking [Continue] in [User Account Control], you can change
  the settings from Property.

* With the default settings of Firewall on Microsoft Windows Vista or later
  versions, data in cross-subnet broadcast cannot be retrieved.
  For cross-subnet data retrieval, please do not use broadcast and specify
  address directly.

* There are feature restrictions below on the execution of Fax print in
  Protected Mode of Microsoft Internet Explorer on Microsoft Windows Vista.
  - A warning message may be displayed right after the execution of Fax print.
  - The location for storage of Fax Phonebook is not a Public Folder, which is
    usually used for storage but a folder such as personal Folder, which can be
    used for file creation. Therefore, the contents of Fax Phonebook are
    different from the one registered with other applications.
  - Import To List feature of Fax Phonebook does not function.

* There is a restriction in creating file from Microsoft Internet Explorer in
  Microsoft Windows Vista. You cannot save form data file in the folder
  specified as the default in [Create / Register Forms]. Change the folder into
  one that can be used for creating file (such as "Document Folder") before
  creating/registering form data file.

* The following functions are restricted with use of Microsoft Internet Explorer
  in Protected Mode on Microsoft Windows Vista or later versions.
  - The setting items for [Job Type] ([Secure Print] / [Sample Set] /
    [Delayed Print] / [Store in Remote Folder]) can not be edited.
  - The functions of [Saved Settings], [Save] and [Edit] are disabled.
  - The functions of [Watermark], [New], [Edit] and [Delete] are disabled.
  - The setting of [Notify Job Completion by E-mail] can not be changed.
  To change the settings of these functions, open the default setting of
  the document from the Printer Folder.

* The remote installation of a print driver from the Print Server to Microsoft
  Windows Vista or later versions may not complete normally. It is recommended
  that you perform the remote installation on Microsoft Windows XP.

* Notes and limitations on Microsoft Windows Vista or later versions
- Server-Client Environment Issue (1)
  If the printer is being used as a shared printer and the server's operating
  system is being upgraded, a message indicating that the driver has to be
  updated may appear on the Windows Vista client, causing printing to fail.
  In this case, the print driver has to be reinstall on the client to be able
  to print again.

- Server-Client Environment Issue (2)
  In the Server-Client environment, after a print driver is added or upgraded
  on the Server side, printing may not be performed with a displayed message
  requiring print driver upgrade on the Client side.
  This problem can be avoided by the settings below.

  < Change of Group Policy Settings on Client PC >
  1. Lon on as an Administrator on Client PC.
  2. Open command prompt and execute "gpedit.msc". to open [Local Group Policy
     Editor].
  3. Open the tree on the left side in the following order.
     [User Configuration]
     [Administrative Templates]
     [Control Panel]
     [Printers]
  4. Double-click [Point and Print Restrictions] in the right pane.
  5. Click the [Disabled] radio button.
     ([Disabled] radio button is on [Settings] tab in Windows Vista.)
  6. Click [OK] to close the window.
  7. Close [Local Group Policy Editor].

  For more details on this issue, please refer to the following URL.
  https://support.microsoft.com/en-us/kb/946225

* Limitation on printing with the settings of Staple and Hole Punch at the same
  time
  Staple and Hole Punch may not function when 1 Staple and Hole Punch are
  specified at the same time for some paper sizes.

* Limitations on Adobe Acrobat/Reader
  When you specify [2] or more pages for [Copies] on the [Print] dialog of
  Adobe Acrobat/Reader, Fax may not be transmitted normally.

* Drawing the Part of Overlapping Image
  Any part or whole of the image may not be printed depending on applications.
  For example, a button or a check box displayed on the Internet Explorer
  screen may not be printed, and nor may be an image attached on the Microsoft
  Word documents printed. In such case, you may be able to solve the problem by
  changing the setting of [Drawing the Overlapping Image] on the [Advanced] tab.

  [Processing 1(Standard)]...Select this option to use the alphablend function
                             without the transparent processing.
  [Processing 2]...Select this option to use the alphablend function and the
                   transparent processing.
  [Processing 3]...Select this option to use the transparent processing without
                   the alphablend function.
  [Processing 4]...Select this option to print an image without using the
                   alphablend function or the transparent processing.

* Annotation and Watermark may not be printed even if [Annotation] and
  [Watermark] are specified.
  To make them function, set [EMF Spooling] to [Enabled] on the [Advanced] tab.

---------------------------------------------------
5. Software Update
---------------------------------------------------
    The latest software is available on our web site.

        http://www.fxap.com.sg/index.jsp

    Communication charges will be borne by the customer.

-------------------------------------------------------------------------------
Microsoft, Windows, Windows Server, Windows Vista, Word, Excel, PowerPoint,
Internet Explorer and Visio are either registered trademarks or trademarks
of Microsoft Corporation in the United States and/or other countries.

Adobe, Acrobat, Illustrator, PageMaker and Reader are
either registered trademarks or trademarks of
Adobe Systems Incorporated in the United States and/or other countries.

CentreWare is a registered trademark of Xerox Corporation.

Other company names and product names are trademarks or registered
trademarks of the respective companies.

This software is based in part on the work of the Independent JPEG Group.

(C) Fuji Xerox Co., Ltd. 2011-2015
