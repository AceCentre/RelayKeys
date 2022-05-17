# Troubleshooting

> Below are solutions to some common issues that you may experience when working with RelayKeys.

{% hint style="info" %}
**AceCentre is a charity and we are providing this as-is. If you need something urgently and can pay we ask you to donate to us - or another developer to help fix your problem**
{% endhint %}

## Installation Issues

### I can install it - but when I send keystrokes nothing is appearing on the second device?

Try and go through these steps:

1. **Is your relaykeys stick properly attached?** Make sure the blue light is showing. If not you may have a loose connection somewhere
2. **Is it paired and connected?** - you will know this if the blue light is steady (_not_ flashing) on the relaykeys stick
3. **check your COM port**. Lastly it may be that the software cannot find the RelayKeys stick in its list of COM ports. [Read this guide](../cli/relaykeys-cfg.html#dev-defining-your-port-of-the-relaykeys-hardware) to manually configure and **fix** your COM port.
4. **Check your casing and spacing**. If you are using the command line applications be careful - the application is case sensitive. it should be _type:_ and not _Type:_ for example

### So I send LSHIFT,2 and I was expecting " but I get a @ - What gives?

We don't support different keyboard layouts yet. Be aware that LSHIFT,' will send " and LSHIFT,2 will send @.
