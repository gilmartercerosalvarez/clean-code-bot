<?php

use Webpt\EmrS3AwsFiles\Dto\ContextDto;
use Webpt\EmrS3AwsFiles\Dto\S3AwsFileDto;
use Webpt\EmrS3AwsFiles\Hydrator\HydrationInterface;
use Wpt\Marshalling\MarshallerInterface;
use function igorw\get_in;

/**
 * Marshaller for S3 AWS file data transfer objects.
 */
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
     * Constructor.
     *
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
     * Marshals the given data into an S3 AWS file data transfer object.
     *
     * @param array $dtoParam
     * @return S3AwsFileDto
     */
    public function marshall(array $dtoParam): S3AwsFileDto
    {
        $contextParam = $this->extractContextParams($dtoParam);
        $context = $this->hydrateContext($contextParam);

        $s3AwsFileParam = $this->extractS3AwsFileParams($dtoParam, $context);
        $s3AwsFileDto = $this->hydrateS3AwsFile($s3AwsFileParam);

        return $s3AwsFileDto;
    }

    /**
     * Extracts context parameters from the given data.
     *
     * @param array $dtoParam
     * @return array
     */
    private function extractContextParams(array $dtoParam): array
    {
        return [
            'company_id' => get_in($dtoParam, ['company_id']),
            'facility_id' => get_in($dtoParam, ['facility_id']),
            'user_id' => get_in($dtoParam, ['user_id']),
            'document_id' => get_in($dtoParam, ['document_id']),
            'patient_id' => get_in($dtoParam, ['patient_id']),
        ];
    }

    /**
     * Hydrates the context data transfer object.
     *
     * @param array $contextParam
     * @return ContextDto
     */
    private function hydrateContext(array $contextParam): ContextDto
    {
        return $this->contextHydratorService->hydrate($contextParam, new ContextDto());
    }

    /**
     * Extracts S3 AWS file parameters from the given data.
     *
     * @param array $dtoParam
     * @param ContextDto $context
     * @return array
     */
    private function extractS3AwsFileParams(array $dtoParam, ContextDto $context): array
    {
        return [
            'bucket_name' => get_in($dtoParam, ['bucket_name'], ''),
            's3_path' => get_in($dtoParam, ['s3_path'], ''),
            'local_path' => get_in($dtoParam, ['local_path'], ''),
            'content' => get_in($dtoParam, ['content'], ''),
            'content_type' => get_in($dtoParam, ['content_type'], ''),
            'context' => $context,
        ];
    }

    /**
     * Hydrates the S3 AWS file data transfer object.
     *
     * @param array $s3AwsFileParam
     * @return S3AwsFileDto
     */
    private function hydrateS3AwsFile(array $s3AwsFileParam): S3AwsFileDto
    {
        return $this->s3AwsFileHydratorService->hydrate($s3AwsFileParam, new S3AwsFileDto());
    }
}