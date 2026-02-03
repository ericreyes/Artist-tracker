import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import { Construct } from 'constructs';

export class ArtistTrackerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB table for artist data
    const artistTable = new dynamodb.Table(this, 'ArtistTable', {
      partitionKey: { name: 'artistId', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'timestamp', type: dynamodb.AttributeType.NUMBER },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Lambda function for API
    const artistFunction = new lambda.Function(this, 'ArtistFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: {
        TABLE_NAME: artistTable.tableName,
      },
    });

    artistTable.grantReadWriteData(artistFunction);

    // API Gateway
    const api = new apigateway.RestApi(this, 'ArtistApi', {
      restApiName: 'Artist Tracker Service',
      description: 'API for tracking artists',
    });

    const artistIntegration = new apigateway.LambdaIntegration(artistFunction);
    api.root.addResource('artists').addMethod('POST', artistIntegration);
  }
}
