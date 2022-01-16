# usage ui2a.py
```
$ ui2a.py mainwindow.ui --classname MainWindow
```
see `ui2a.py -h` for poor details.

# example for result (stdout)
Suppose you make actions named actionConnect, actionDisconnect, actionViewDot(has checkable) using Qt Designer.

ui2a.py puts following to stdout:
```
 <connections>
  <connection>
   <sender>actionConnect</sender>
   <signal>triggered()</signal>
   <receiver>MainWindowClass</receiver>
   <slot>actionConnect()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>-1</x>
     <y>-1</y>
    </hint>
    <hint type="destinationlabel">
     <x>0</x>
     <y>0</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>actionDisconnect</sender>
   <signal>triggered()</signal>
   <receiver>MainWindowClass</receiver>
   <slot>actionDisconnect()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>-1</x>
     <y>-1</y>
    </hint>
    <hint type="destinationlabel">
     <x>0</x>
     <y>0</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>actionViewDot</sender>
   <signal>triggered(bool)</signal>
   <receiver>MainWindowClass</receiver>
   <slot>actionViewDot(bool)</slot>
   <hints>
    <hint type="sourcelabel">
     <x>-1</x>
     <y>-1</y>
    </hint>
    <hint type="destinationlabel">
     <x>0</x>
     <y>0</y>
    </hint>
   </hints>
  </connection>
 </connections>
 <slots>
  <slot>actionConnect()</slot>
  <slot>actionDisconnect()</slot>
  <slot>actionViewDot(bool)</slot>
 </slots>

 public slots:
  void actionConnect();
  void actionDisconnect();
  void actionViewDot(bool checked);

void MainWindow::actionConnect() {}
void MainWindow::actionDisconnect() {}
void MainWindow::actionViewDot(bool checked) {}
```
You can copy and paste this text to your .h, .cpp and .ui files.<br>
When you edit the .ui file, be careful not to break it.

`<connections>` and `<slots>` are elements required by the .ui file.
