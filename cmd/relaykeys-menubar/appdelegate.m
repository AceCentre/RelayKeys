#import <Cocoa/Cocoa.h>

extern void goClickOpen();
extern void goClickCapture();
extern void goClickQuit();
extern void goClickSwitch();

@interface AppDelegate : NSObject <NSApplicationDelegate>
@property (strong) NSStatusItem *statusItem;
@property (strong) NSMenu *menu;
@property (strong) NSAttributedString *titleConnected;
@property (strong) NSAttributedString *titleDisconnected;
@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    [NSApp setActivationPolicy:2];

    self.statusItem = [[NSStatusBar systemStatusBar] statusItemWithLength:NSVariableStatusItemLength];
    self.statusItem.button.toolTip = @"RelayKeys";

    self.menu = [[NSMenu alloc] init];

    NSMenuItem *statusItem = [[NSMenuItem alloc] initWithTitle:@"Device: ..." action:nil keyEquivalent:@""];
    statusItem.tag = 100;
    [self.menu addItem:statusItem];

    [self.menu addItem:[NSMenuItem separatorItem]];

    NSMenuItem *openItem = [[NSMenuItem alloc] initWithTitle:@"Open Web UI" action:@selector(clickOpen:) keyEquivalent:@"o"];
    [openItem setTarget:self];
    [self.menu addItem:openItem];

    NSMenuItem *captureItem = [[NSMenuItem alloc] initWithTitle:@"Toggle Capture" action:@selector(clickCapture:) keyEquivalent:@"c"];
    [captureItem setTarget:self];
    [self.menu addItem:captureItem];

    NSMenuItem *switchItem = [[NSMenuItem alloc] initWithTitle:@"Switch Device" action:@selector(clickSwitch:) keyEquivalent:@"s"];
    [switchItem setTarget:self];
    [self.menu addItem:switchItem];

    [self.menu addItem:[NSMenuItem separatorItem]];

    NSMenuItem *quitItem = [[NSMenuItem alloc] initWithTitle:@"Quit RelayKeys" action:@selector(clickQuit:) keyEquivalent:@"q"];
    [quitItem setTarget:self];
    [self.menu addItem:quitItem];

    self.statusItem.menu = self.menu;

    NSDictionary *attrsOn = @{NSFontAttributeName: [NSFont boldSystemFontOfSize:13], NSForegroundColorAttributeName: [NSColor systemGreenColor]};
    NSDictionary *attrsOff = @{NSFontAttributeName: [NSFont boldSystemFontOfSize:13], NSForegroundColorAttributeName: [NSColor systemRedColor]};
    self.titleConnected = [[NSAttributedString alloc] initWithString:@"RK" attributes:attrsOn];
    self.titleDisconnected = [[NSAttributedString alloc] initWithString:@"RK" attributes:attrsOff];
    self.statusItem.button.attributedTitle = self.titleDisconnected;
}

- (IBAction)clickOpen:(id)sender { goClickOpen(); }
- (IBAction)clickCapture:(id)sender { goClickCapture(); }
- (IBAction)clickQuit:(id)sender { goClickQuit(); }
- (IBAction)clickSwitch:(id)sender { goClickSwitch(); }

- (void)updateStatus:(NSString *)device connected:(BOOL)connected {
    dispatch_async(dispatch_get_main_queue(), ^{
        self.statusItem.button.attributedTitle = connected ? self.titleConnected : self.titleDisconnected;
        NSMenuItem *statusItem = [self.menu itemWithTag:100];
        if (statusItem) {
            statusItem.title = connected ? [NSString stringWithFormat:@"Device: %@", device] : @"Not connected";
        }
    });
}

@end

void runMenuBarApp() {
    [NSApplication sharedApplication];
    AppDelegate *delegate = [[AppDelegate alloc] init];
    [NSApp setDelegate:delegate];
    [NSApp run];
}

void cocoaUpdateStatus(const char* device, int connected) {
    AppDelegate *delegate = (AppDelegate *)[NSApp delegate];
    [delegate updateStatus:[NSString stringWithUTF8String:device] connected:connected];
}
