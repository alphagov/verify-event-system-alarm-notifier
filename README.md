# verify-event-system-alarm-notifier

Lambda function for notifying in Slack when CloudWatch alarms are triggered in the Event System.

## Release

### Automated release

The code in this repository gets built and deployed to the Lambda function, as part of a continuous
integration and deployment (CI/CD) pipeline in Concourse, upon merge into the `master` branch.

### Manual release

If, for any reason, you need to manually deploy the code, package it up by running the following
script:

```bash
./build/package.sh
```

This creates a zip archive of the source code, along with all of the dependencies, ready to be
uploaded to the Lambda function. The script does all of this within a Docker container, which has the
benefit of keeping the build environment closer to the actual Lambda runtime environment than our
development laptops. This is useful, for example, in case there are Python libraries being used which
rely on platform specific binaries, meaning the ones installed on our development laptops won't work
on the Lambda runtime environment.

Once the above script has created a zip archive, upload it manually to the Lambda function (either
from the AWS Web Console or by using the AWS CLI).

Note that the automated release process mentioned earlier makes use of this script internally as
part of the pipeline.