'use strict';

const fs = require('fs');
var path = require('path');
const aws = require('aws-sdk');
var s3 = new aws.S3({
    accessKeyId: 'minioadmin' ,
    secretAccessKey: 'minioadmin' ,
    endpoint: 'http://minio:9000' ,
    s3ForcePathStyle: true, // needed with minio?
    signatureVersion: 'v4'
});
var util = require('util');
let execSync = require('child_process').execSync;

var i = 1;
const getObject = function(bucket, key, resolve, preserve) {
  let params = {
    Bucket: bucket,
    Key: key
  };
  s3.getObject(params, function(error, data) {
    try {
      if (error) {
        preserve(error);
      } else {
        resolve(data);
      }
    } catch(e) {
      preserve(e);
    }
  });
};

const putObject = function(body, bucket, key, resolve, preserve) {
  let params = {
    Body: body,
    Bucket: bucket,
    Key: key
  };

  s3.putObject(params, function(error, data) {
    try {
      if (error) {
        preserve(error);
      } else {
        resolve(data);
      }
    } catch(e) {
      preserve(e);
    }
  });
};

exports.handler = (event, context, callback) => {
  try {
    //console.log("EVENT: \n" + JSON.stringify(event, null, 2));

    //var srcKey = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, " "));
    //var name =  path.basename(srcKey, path.extname(srcKey));

    var bucketName = event.Records[0].s3.bucket.name;
    console.log('==== bucket information =====');
    console.log(bucketName);
    console.log('=============================');

    var uplodedFile = event.Records[0].s3.object.key;
    console.log('==== uploaded file ====');
    console.log(uplodedFile);
    console.log('=============================');

    getObject(bucketName, uplodedFile, function(srcData) {        
      
      console.log("get object");
      fs.writeFileSync('/tmp/srcData.mp4', srcData.Body);

      process.env.PATH += ':/var/task/bin';
      execSync('ffmpeg -i /tmp/srcData.mp4 -filter:v fps=fps=1:round=down /tmp/%d.jpg');

      var files = fs.readdirSync('/tmp');

      for (var i = 1; i <= files.length - 1; i++) {
        var fileStream = fs.createReadStream('/tmp/'+ i +'.jpg');
        putObject(fileStream, bucketName, 'Output/output' + i +'.jpg', function(data) {
          callback(null, 'OK');
        });
      }
    });
  } catch(e) {
    callback(JSON.stringify(e));
  }
};
