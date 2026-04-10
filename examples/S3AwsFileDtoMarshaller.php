<?php


use Webpt\EmrS3AwsFiles\Dto\ContextDto;
use Webpt\EmrS3AwsFiles\Dto\S3AwsFileDto;
use Webpt\EmrS3AwsFiles\Hydrator\HydrationInterface;
use Wpt\Marshalling\MarshallerInterface;
use function igorw\get_in;

class S3AwsFileDtoMarshaller implements MarshallerInterface
{
    /**
     * @var HydrationInterface
     */
    private $contextHydratorService;

    /**
     * @var HydrationInterface
     */
    private $s3AwsFileHydratorService;

    /**
     * @param HydrationInterface $s3AwsFileHydratorService
     * @param HydrationInterface $contextHydratorService
     */
    public function __construct(
        HydrationInterface $s3AwsFileHydratorService,
        HydrationInterface $contextHydratorService
    ) {
        $this->s3AwsFileHydratorService = $s3AwsFileHydratorService;
        $this->contextHydratorService = $contextHydratorService;
    }

    /**
     * @param array $dtoParam
     * @return S3AwsFileDto
     */
    public function marshall($dtoParam)
    {
        $contextParam = [
            'company_id' => get_in($dtoParam, ['company_id']),
            'facility_id' => get_in($dtoParam, ['facility_id']),
            'user_id' => get_in($dtoParam, ['user_id']),
            'document_id' => get_in($dtoParam, ['document_id']),
            'patient_id' => get_in($dtoParam, ['patient_id']),
        ];
        /** @var ContextDto $context */
        $context = $this->contextHydratorService->hydrate($contextParam, new ContextDto());
        $s3AwsFileParam = [
            'bucket_name' => get_in($dtoParam, ['bucket_name'], ''),
            's3_path' => get_in($dtoParam, ['s3_path'], ''),
            'local_path' => get_in($dtoParam, ['local_path'], ''),
            'content' => get_in($dtoParam, ['content'], ''),
            'content_type' => get_in($dtoParam, ['content_type'], ''),
            'context' => $context,
        ];
        /** @var S3AwsFileDto $s3AwsFileDto */
        $s3AwsFileDto = $this->s3AwsFileHydratorService->hydrate($s3AwsFileParam, new S3AwsFileDto());

        return $s3AwsFileDto;
    }
}

